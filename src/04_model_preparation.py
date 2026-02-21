import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import json
import os

def prepare_data():
    print("Loading customer features...")
    df = pd.read_csv('data/processed/customer_features.csv')
    
    target_col = 'Churn' if 'Churn' in df.columns else 'churn'
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")
        
    print(f"Original shape: {df.shape}")
    
    # Extract CustomerID but keep it aligned later if needed
    customer_ids = df['CustomerID']
    
    # 2. Separate features and target
    y = df[target_col]
    X_raw = df.drop(['CustomerID', target_col], axis=1)
    
    # 3. Categorical encoding
    print("Encoding categorical variables...")
    cat_columns = X_raw.select_dtypes(include=['object', 'category']).columns.tolist()
    if 'CustomerSegment' in X_raw.columns and 'CustomerSegment' not in cat_columns:
        cat_columns.append('CustomerSegment')
        
    print(f"Categorical columns identified: {cat_columns}")
    X_encoded = pd.get_dummies(X_raw, columns=cat_columns, drop_first=False)
    
    # Save feature names
    feature_names = X_encoded.columns.tolist()
    
    # 4. Train/Validation/Test Split (70/15/15)
    print("Splitting data into Train/Val/Test...")
    X_temp, X_test, y_temp, y_test = train_test_split(
        X_encoded, y, test_size=0.15, stratify=y, random_state=42
    )
    
    # Adjust valid size to be 15% of total. 15 / 85 = 0.17647
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.17647, stratify=y_temp, random_state=42
    )
    
    # 5. Scale numerical features
    print("Scaling numerical features...")
    scaler = StandardScaler()
    
    # Fit scaler only on numerical columns that are not one-hot encoded (booleans/uint8 usually)
    bool_cols = X_train.select_dtypes(include=['boolean', 'bool']).columns.tolist()
    # Let's just scale everything that is numeric and not in bool_cols
    numeric_features = [c for c in feature_names if c not in bool_cols and not (X_train[c].nunique() <= 2)]
    
    print(f"Applying StandardScaler to {len(numeric_features)} continuous features...")
    
    X_train_scaled = X_train.copy()
    X_val_scaled = X_val.copy()
    X_test_scaled = X_test.copy()
    
    if len(numeric_features) > 0:
        X_train_scaled[numeric_features] = scaler.fit_transform(X_train[numeric_features])
        X_val_scaled[numeric_features] = scaler.transform(X_val[numeric_features])
        X_test_scaled[numeric_features] = scaler.transform(X_test[numeric_features])
    
    # 6. Save data
    print("Saving prepared datasets...")
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    X_train_scaled.to_csv('data/processed/X_train.csv', index=False)
    X_val_scaled.to_csv('data/processed/X_val.csv', index=False)
    X_test_scaled.to_csv('data/processed/X_test.csv', index=False)
    
    pd.DataFrame(y_train).to_csv('data/processed/y_train.csv', index=False)
    pd.DataFrame(y_val).to_csv('data/processed/y_val.csv', index=False)
    pd.DataFrame(y_test).to_csv('data/processed/y_test.csv', index=False)
    
    joblib.dump(scaler, 'models/scaler.pkl')
    
    with open('data/processed/feature_names.json', 'w') as f:
        json.dump(feature_names, f, indent=4)
        
    print("\nData Preparation Summary:")
    print(f"- Original features: {X_raw.shape[1]}")
    print(f"- Features after encoding: {X_encoded.shape[1]}")
    print(f"- Training samples: {len(X_train)}")
    print(f"- Validation samples: {len(X_val)}")
    print(f"- Test samples: {len(X_test)}")
    print(f"- Churn rate in train: {y_train.mean()*100:.2f}%")
    print(f"- Churn rate in test: {y_test.mean()*100:.2f}%")

if __name__ == "__main__":
    prepare_data()
