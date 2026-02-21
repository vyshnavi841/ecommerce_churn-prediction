import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class FeatureEngineer:
    """
    Transform transaction data into customer-level features
    """
    def __init__(self, transactions_path='data/processed/cleaned_transactions.csv'):
        self.transactions = pd.read_csv(transactions_path, parse_dates=['InvoiceDate'])
        # DYNAMIC APPROACH:
        self.observation_end = self.transactions['InvoiceDate'].max()
        self.training_cutoff = self.observation_end - pd.Timedelta(days=90)
        self.training_data = None
        self.observation_data = None
        self.customer_features = None
        
        print(f"Loaded {len(self.transactions)} transactions")
        print(f"Training cutoff: {self.training_cutoff}")
        print(f"Observation end: {self.observation_end}")
    
    def split_data_by_time(self):
        print("\nSplitting data into training and observation periods...")
        self.training_data = self.transactions[self.transactions['InvoiceDate'] <= self.training_cutoff].copy()
        self.observation_data = self.transactions[(self.transactions['InvoiceDate'] > self.training_cutoff) &
                                                  (self.transactions['InvoiceDate'] <= self.observation_end)].copy()
        print(f"Training transactions: {len(self.training_data)}")
        print(f"Observation transactions: {len(self.observation_data)}")
        return self
    
    def create_target_variable(self):
        print("\nCreating target variable (Churn)...")
        training_customers = set(self.training_data['CustomerID'].unique())
        observation_customers = set(self.observation_data['CustomerID'].unique())
        
        self.customer_features = pd.DataFrame({'CustomerID': list(training_customers)})
        self.customer_features['Churn'] = self.customer_features['CustomerID'].apply(
            lambda x: 1 if x not in observation_customers else 0
        )
        churn_rate = self.customer_features['Churn'].mean() * 100
        print(f"Churn rate: {churn_rate:.2f}%")
        return self
    
    def create_rfm_features(self):
        print("\nCreating RFM features...")
        df = self.training_data.copy()
        
        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (self.training_cutoff - x.max()).days,
            'InvoiceNo': 'nunique',
            'TotalPrice': ['sum', 'mean'],
            'StockCode': 'nunique',
            'Quantity': 'sum'
        }).reset_index()
        
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'TotalSpent', 'AvgOrderValue', 'UniqueProducts', 'TotalItems']
        self.customer_features = self.customer_features.merge(rfm, on='CustomerID', how='left')
        return self
    
    def create_behavioral_features(self):
        print("\nCreating behavioral features...")
        df = self.training_data.copy()
        
        # AvgDaysBetweenPurchases
        purchases = df[['CustomerID', 'InvoiceNo', 'InvoiceDate']].drop_duplicates()
        intervals = purchases.sort_values('InvoiceDate').groupby('CustomerID')['InvoiceDate'].diff().dt.days
        purchases['Interval'] = intervals
        avg_intervals = purchases.groupby('CustomerID')['Interval'].mean().reset_index()
        avg_intervals.columns = ['CustomerID', 'AvgDaysBetweenPurchases']
        
        # Basket size
        basket_size = df.groupby(['CustomerID', 'InvoiceNo'])['Quantity'].sum().reset_index()
        basket_stats = basket_size.groupby('CustomerID')['Quantity'].agg(['mean', 'std', 'max']).reset_index()
        basket_stats.columns = ['CustomerID', 'AvgBasketSize', 'StdBasketSize', 'MaxBasketSize']
        
        # Time prefs
        time_prefs = df.groupby('CustomerID').agg({
            'DayOfWeek': lambda x: x.mode()[0] if not x.mode().empty else np.nan,
            'Hour': lambda x: x.mode()[0] if not x.mode().empty else np.nan
        }).reset_index()
        time_prefs.columns = ['CustomerID', 'PreferredDay', 'PreferredHour']
        
        # Country
        country_diversity = df.groupby('CustomerID')['Country'].nunique().reset_index()
        country_diversity.columns = ['CustomerID', 'CountryDiversity']
        
        self.customer_features = self.customer_features.merge(avg_intervals, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(basket_stats, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(time_prefs, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(country_diversity, on='CustomerID', how='left')
        return self
    
    def create_temporal_features(self):
        print("\nCreating temporal features...")
        df = self.training_data.copy()
        
        lifetime = df.groupby('CustomerID').agg({'InvoiceDate': ['min', 'max']}).reset_index()
        lifetime.columns = ['CustomerID', 'FirstPurchaseDate', 'LastPurchaseDate']
        lifetime['CustomerLifetimeDays'] = (lifetime['LastPurchaseDate'] - lifetime['FirstPurchaseDate']).dt.days
        
        temp_features_df = lifetime[['CustomerID', 'CustomerLifetimeDays']].copy()
        
        merged_freq = self.customer_features[['CustomerID', 'Frequency']]
        temp_features_df = temp_features_df.merge(merged_freq, on='CustomerID')
        temp_features_df['PurchaseVelocity'] = temp_features_df['Frequency'] / (temp_features_df['CustomerLifetimeDays'] + 1.0)
        temp_features_df = temp_features_df.drop('Frequency', axis=1)

        cutoff_30 = self.training_cutoff - timedelta(days=30)
        cutoff_60 = self.training_cutoff - timedelta(days=60)
        cutoff_90 = self.training_cutoff - timedelta(days=90)
        
        recent_30 = df[df['InvoiceDate'] > cutoff_30].groupby('CustomerID')['InvoiceNo'].nunique().reset_index(name='Purchases_Last30Days')
        recent_60 = df[df['InvoiceDate'] > cutoff_60].groupby('CustomerID')['InvoiceNo'].nunique().reset_index(name='Purchases_Last60Days')
        recent_90 = df[df['InvoiceDate'] > cutoff_90].groupby('CustomerID')['InvoiceNo'].nunique().reset_index(name='Purchases_Last90Days')
        
        self.customer_features = self.customer_features.merge(temp_features_df, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(recent_30, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(recent_60, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(recent_90, on='CustomerID', how='left')
        
        self.customer_features[['Purchases_Last30Days', 'Purchases_Last60Days', 'Purchases_Last90Days']] = \
            self.customer_features[['Purchases_Last30Days', 'Purchases_Last60Days', 'Purchases_Last90Days']].fillna(0)
            
        return self
    
    def create_product_features(self):
        print("\nCreating product features...")
        df = self.training_data.copy()
        
        product_diversity = df.groupby('CustomerID').agg({'StockCode': lambda x: len(set(x)) / len(x)}).reset_index()
        product_diversity.columns = ['CustomerID', 'ProductDiversityScore']
        
        price_pref = df.groupby('CustomerID')['UnitPrice'].agg(['mean', 'std', 'min', 'max']).reset_index()
        price_pref.columns = ['CustomerID', 'AvgPricePreference', 'StdPricePreference', 'MinPrice', 'MaxPrice']
        
        qty_pref = df.groupby(['CustomerID', 'InvoiceNo'])['Quantity'].sum().reset_index()
        qty_stats = qty_pref.groupby('CustomerID')['Quantity'].mean().reset_index(name='AvgQuantityPerOrder')
        
        self.customer_features = self.customer_features.merge(product_diversity, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(price_pref, on='CustomerID', how='left')
        self.customer_features = self.customer_features.merge(qty_stats, on='CustomerID', how='left')
        return self
    
    def create_customer_value_segment(self):
        print("\nCreating customer value segments...")
        
        self.customer_features['RecencyScore'] = pd.qcut(self.customer_features['Recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop').astype(int)
        # Note: Some frequencies might be highly identical, thus drop
        freq_bins = pd.qcut(self.customer_features['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
        self.customer_features['FrequencyScore'] = freq_bins
        self.customer_features['MonetaryScore'] = pd.qcut(self.customer_features['TotalSpent'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
        
        self.customer_features['RFM_Score'] = (self.customer_features['RecencyScore'] + 
                                               self.customer_features['FrequencyScore'] + 
                                               self.customer_features['MonetaryScore'])
        
        def rfm_segment(row):
            if row['RFM_Score'] >= 10: return 'Champions'
            elif row['RFM_Score'] >= 8: return 'Loyal'
            elif row['RFM_Score'] >= 6: return 'Potential'
            elif row['RFM_Score'] >= 4: return 'At Risk'
            else: return 'Lost'
            
        self.customer_features['CustomerSegment'] = self.customer_features.apply(rfm_segment, axis=1)
        return self
    
    def handle_missing_values(self):
        print("\nHandling missing values in features...")
        numeric_cols = self.customer_features.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['CustomerID', 'Churn']:
                self.customer_features[col] = self.customer_features[col].fillna(self.customer_features[col].median())
                
        cat_cols = self.customer_features.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            self.customer_features[col] = self.customer_features[col].fillna(self.customer_features[col].mode()[0])
            
        return self
    
    def save_features(self, output_path='data/processed/customer_features.csv'):
        print("\nSaving customer features...")
        os.makedirs('data/processed', exist_ok=True)
        self.customer_features.to_csv(output_path, index=False)
        
        feature_info = {
            'total_customers': len(self.customer_features),
            'total_features': len(self.customer_features.columns) - 2,
            'churn_rate': float(self.customer_features['Churn'].mean()),
            'feature_list': list(self.customer_features.columns),
            'feature_categories': {
                'rfm': ['Recency', 'Frequency', 'TotalSpent', 'AvgOrderValue', 'UniqueProducts', 'TotalItems'],
                'behavioral': ['AvgDaysBetweenPurchases', 'AvgBasketSize', 'StdBasketSize', 'MaxBasketSize', 
                              'PreferredDay', 'PreferredHour', 'CountryDiversity'],
                'temporal': ['CustomerLifetimeDays', 'PurchaseVelocity', 'Purchases_Last30Days', 
                            'Purchases_Last60Days', 'Purchases_Last90Days'],
                'product': ['ProductDiversityScore', 'AvgPricePreference', 'StdPricePreference', 
                           'MinPrice', 'MaxPrice', 'AvgQuantityPerOrder'],
                'segmentation': ['RecencyScore', 'FrequencyScore', 'MonetaryScore', 'RFM_Score', 'CustomerSegment']
            }
        }
        
        with open('data/processed/feature_info.json', 'w') as f:
            json.dump(feature_info, f, indent=4)
            
        return self
    
    def run_pipeline(self):
        self.split_data_by_time()
        self.create_target_variable()
        self.create_rfm_features()
        self.create_behavioral_features()
        self.create_temporal_features()
        self.create_product_features()
        self.create_customer_value_segment()
        self.handle_missing_values()
        self.save_features()
        print("Pipeline complete")
        return self.customer_features

if __name__ == "__main__":
    engineer = FeatureEngineer('data/processed/cleaned_transactions.csv')
    customer_features = engineer.run_pipeline()
