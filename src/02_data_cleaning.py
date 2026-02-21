import pandas as pd
import numpy as np
import json
import logging
import os

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCleaner:
    """
    Comprehensive data cleaning pipeline for Online Retail dataset
    """
    
    def __init__(self, input_path='data/raw/online_retail.csv'):
        self.input_path = input_path
        self.df = None
        self.cleaning_stats = {
            'original_rows': 0,
            'rows_after_cleaning': 0,
            'rows_removed': 0,
            'missing_values_before': {},
            'missing_values_after': {},
            'steps_applied': []
        }
    
    def load_data(self):
        logging.info("Loading raw dataset...")
        self.df = pd.read_csv(
            self.input_path,
            encoding='latin1',
            parse_dates=['InvoiceDate']
        )
        
        self.cleaning_stats['original_rows'] = len(self.df)
        self.cleaning_stats['missing_values_before'] = self.df.isnull().sum().to_dict()
        logging.info(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        return self
    
    def remove_missing_customer_ids(self):
        logging.info("Step 1: Removing missing CustomerIDs...")
        initial_rows = len(self.df)
        
        self.df = self.df.dropna(subset=['CustomerID'])
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with missing CustomerID")
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_missing_customer_ids',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_cancelled_invoices(self):
        logging.info("Step 2: Handling cancelled invoices...")
        initial_rows = len(self.df)
        
        self.df = self.df[~self.df['InvoiceNo'].astype(str).str.contains('C', na=False)]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} cancelled invoices")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_cancelled_invoices',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_negative_quantities(self):
        logging.info("Step 3: Handling negative quantities...")
        initial_rows = len(self.df)
        
        self.df = self.df[self.df['Quantity'] > 0]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with negative quantities")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_negative_quantities',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_zero_prices(self):
        logging.info("Step 4: Removing zero/negative prices...")
        initial_rows = len(self.df)
        
        self.df = self.df[self.df['UnitPrice'] > 0]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with invalid prices")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_zero_prices',
            'rows_removed': rows_removed
        })
        return self
    
    def handle_missing_descriptions(self):
        logging.info("Step 5: Handling missing descriptions...")
        initial_rows = len(self.df)
        
        self.df = self.df.dropna(subset=['Description'])
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} rows with missing descriptions")
        self.cleaning_stats['steps_applied'].append({
            'step': 'handle_missing_descriptions',
            'rows_removed': rows_removed
        })
        return self
    
    def remove_outliers(self):
        logging.info("Step 6: Removing outliers using IQR method...")
        initial_rows = len(self.df)
        
        # Quantity outliers
        Q1_qty = self.df['Quantity'].quantile(0.25)
        Q3_qty = self.df['Quantity'].quantile(0.75)
        IQR_qty = Q3_qty - Q1_qty
        lower_bound_qty = Q1_qty - 1.5 * IQR_qty
        upper_bound_qty = Q3_qty + 1.5 * IQR_qty
        
        self.df = self.df[(self.df['Quantity'] >= lower_bound_qty) & (self.df['Quantity'] <= upper_bound_qty)]
        
        # Price outliers (using an upper bound of 3*IQR to be less aggressive and preserve high value purchases)
        Q1_price = self.df['UnitPrice'].quantile(0.25)
        Q3_price = self.df['UnitPrice'].quantile(0.75)
        IQR_price = Q3_price - Q1_price
        upper_bound_price = Q3_price + 3.0 * IQR_price
        
        self.df = self.df[self.df['UnitPrice'] <= upper_bound_price]
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} outlier rows")
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_outliers',
            'rows_removed': rows_removed,
            'method': 'IQR',
            'threshold': 'Qty: 1.5, Price: 3.0'
        })
        return self
    
    def remove_duplicates(self):
        logging.info("Step 7: Removing duplicates...")
        initial_rows = len(self.df)
        
        self.df = self.df.drop_duplicates()
        
        rows_removed = initial_rows - len(self.df)
        logging.info(f"Removed {rows_removed} duplicate rows")
        self.cleaning_stats['steps_applied'].append({
            'step': 'remove_duplicates',
            'rows_removed': rows_removed
        })
        return self
    
    def add_derived_columns(self):
        logging.info("Step 8: Creating derived columns...")
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['UnitPrice']
        self.df['Year'] = self.df['InvoiceDate'].dt.year
        self.df['Month'] = self.df['InvoiceDate'].dt.month
        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.dayofweek
        self.df['Hour'] = self.df['InvoiceDate'].dt.hour
        
        self.cleaning_stats['steps_applied'].append({
            'step': 'add_derived_columns',
            'columns_added': ['TotalPrice', 'Year', 'Month', 'DayOfWeek', 'Hour']
        })
        return self
    
    def convert_data_types(self):
        logging.info("Step 9: Converting data types...")
        self.df['CustomerID'] = self.df['CustomerID'].astype(int)
        self.df['StockCode'] = self.df['StockCode'].astype('category')
        self.df['Country'] = self.df['Country'].astype('category')
        
        self.cleaning_stats['steps_applied'].append({
            'step': 'convert_data_types'
        })
        return self
    
    def save_cleaned_data(self, output_path='data/processed/cleaned_transactions.csv'):
        logging.info("Saving cleaned data...")
        os.makedirs('data/processed', exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        logging.info(f"Cleaned data saved to: {output_path}")
        
        self.cleaning_stats['rows_after_cleaning'] = len(self.df)
        self.cleaning_stats['rows_removed'] = (
            self.cleaning_stats['original_rows'] - 
            self.cleaning_stats['rows_after_cleaning']
        )
        self.cleaning_stats['retention_rate'] = round(len(self.df) / self.cleaning_stats['original_rows'] * 100, 2)
        self.cleaning_stats['missing_values_after'] = self.df.isnull().sum().to_dict()
        
        with open('data/processed/cleaning_statistics.json', 'w') as f:
            json.dump(self.cleaning_stats, f, indent=4, default=str)
        
        print("\n" + "="*50)
        print("DATA CLEANING SUMMARY")
        print("="*50)
        print(f"Original rows: {self.cleaning_stats['original_rows']:,}")
        print(f"Cleaned rows: {self.cleaning_stats['rows_after_cleaning']:,}")
        print(f"Rows removed: {self.cleaning_stats['rows_removed']:,}")
        print(f"Retention rate: {self.cleaning_stats['retention_rate']}%")
        print("="*50)
        
        return self
    
    def run_pipeline(self):
        print("Starting data cleaning pipeline...")
        self.load_data()
        self.remove_missing_customer_ids()
        self.handle_cancelled_invoices()
        self.handle_negative_quantities()
        self.handle_zero_prices()
        self.handle_missing_descriptions()
        self.remove_outliers()
        self.remove_duplicates()
        self.add_derived_columns()
        self.convert_data_types()
        self.save_cleaned_data()
        print("Data cleaning pipeline completed successfully!")
        return self.df

if __name__ == "__main__":
    cleaner = DataCleaner('data/raw/online_retail.csv')
    cleaned_df = cleaner.run_pipeline()
    
    print(f"\nCleaned dataset shape: {cleaned_df.shape}")
    print(f"Columns: {list(cleaned_df.columns)}")
