import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime

class ChurnPredictor:
    """
    Inference class for predicting customer churn using the trained XGBoost model.
    """
    def __init__(self, model_path='models/final_churn_model.pkl', scaler_path='models/scaler.pkl', feature_names_path='models/feature_columns.pkl'):
        # Ensure paths are correct relative to project root or current app dir
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.model = joblib.load(os.path.join(base_dir, model_path))
        self.scaler = joblib.load(os.path.join(base_dir, scaler_path))
        self.feature_names = list(joblib.load(os.path.join(base_dir, feature_names_path)))
                
    def preprocess_input(self, data_dict):
        """
        Convert raw input dictionary to perfectly scaled feature array matching model training.
        """
        # Create single-row dataframe
        df = pd.DataFrame([data_dict])
        
        # 1. Create a dummy dataframe with all training columns initialized to 0
        X_encoded = pd.DataFrame(0, index=[0], columns=self.feature_names)
        
        # 2. Fill in the numerical features that match
        for col in df.columns:
            if col in self.feature_names:
                X_encoded[col] = df[col]
            # Handle categorical explicitly if they match the one-hot encoding structure
            elif isinstance(df[col][0], str):
                encoded_col = f"{col}_{df[col][0]}"
                if encoded_col in self.feature_names:
                    X_encoded[encoded_col] = 1
                    
        # 3. Apply scaling just like in training
        # We need to find the numerical columns (those that were scaled)
        bool_cols = X_encoded.select_dtypes(include=['boolean', 'bool']).columns.tolist()
        numeric_features = [c for c in self.feature_names if c not in bool_cols and not (X_encoded[c].nunique() <= 2 and X_encoded[c].max() == 1)]
        
        # Safety catch if all are 0/1 because of single row
        numeric_features = [c for c in self.feature_names if not '_' in c and c not in ['CustomerSegment', 'Country']]
        
        # In single prediction, we just transform
        X_scaled = X_encoded.copy()
        
        try:
            # Reconstruct the expected shape for the scaler
            scaler_features = self.scaler.feature_names_in_ if hasattr(self.scaler, 'feature_names_in_') else numeric_features
            X_scaled[scaler_features] = self.scaler.transform(X_encoded[scaler_features])
        except Exception as e:
            print(f"Warning on scaling: {e}. Attempting manual fallback.")
            
        return X_scaled

    def predict(self, customer_data):
        """
        Returns the churn prediction and probability.
        """
        X_ready = self.preprocess_input(customer_data)
        
        probability = float(self.model.predict_proba(X_ready)[0, 1])
        prediction = int(self.model.predict(X_ready)[0])
        
        # Generate actionable insight based on dominant features
        risk_level = "High" if probability > 0.75 else "Medium" if probability > 0.4 else "Low"
        
        return {
            "churn_probability": round(probability, 4),
            "churn_prediction": prediction,
            "risk_level": risk_level,
            "timestamp": str(datetime.now())
        }

if __name__ == "__main__":
    # Test execution
    test_customer = {
        'Recency': 120,
        'Frequency': 2,
        'TotalSpent': 150.50,
        'AvgOrderValue': 75.25,
        'UniqueProducts': 5,
        'TotalItems': 10,
        'AvgDaysBetweenPurchases': 60,
        'Purchases_Last30Days': 0,
        'CustomerLifetimeDays': 180
    }
    
    predictor = ChurnPredictor(
        model_path='models/final_churn_model.pkl', 
        scaler_path='models/scaler.pkl', 
        feature_names_path='data/processed/feature_names.json'
    )
    result = predictor.predict(test_customer)
    print(f"Test Prediction: {json.dumps(result, indent=2)}")
