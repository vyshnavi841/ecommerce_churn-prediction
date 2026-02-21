import pandas as pd
import requests
import os
from datetime import datetime

def download_dataset():
    """
    Download the Online Retail dataset
    Save to data/raw/online_retail.csv
    
    HINT: Use pandas read_excel or read_csv
    HINT: Handle potential download failures
    """

    """
    REQUIRED DATASET:
    - File: online_retail_II.xlsx (or Year 2010-2011.xlsx)
    - Download from: http://archive.ics.uci.edu/ml/machine-learning-databases/00502/
    - If UCI is down, use Kaggle: https://www.kaggle.com/datasets/carrie1/ecommerce-data
    - Expected rows: 541,909 rows
    """
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"
    csv_path = 'data/raw/online_retail.csv'
    
    # Create directory structure
    os.makedirs('data/raw', exist_ok=True)
    
    if os.path.exists(csv_path):
        print(f"Dataset already exists at {csv_path}")
        return True
        
    print(f"Downloading dataset from {url}...")
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        xlsx_path = 'data/raw/online_retail_II.xlsx'
        with open(xlsx_path, 'wb') as f:
            f.write(response.content)
            
        print("Converting to CSV... This might take a minute.")
        # The dataset has two sheets, we need 'Year 2010-2011' to get the ~541,909 rows
        df = pd.read_excel(xlsx_path, sheet_name='Year 2010-2011')
        df.to_csv(csv_path, index=False)
        print("Dataset converted to CSV successfully.")
        
    except Exception as e:
        print(f"Error downloading: {e}")
        return False
    
    print(f"Dataset downloaded: {datetime.now()}")
    print(f"Saved to: {csv_path}")
    
    return True

def load_raw_data():
    """
    Load the raw dataset and return DataFrame
    
    Returns:
        pd.DataFrame: Raw dataset
    """
    df = pd.read_csv('data/raw/online_retail.csv')
    return df

def generate_data_profile(df=None):
    """
    Generate initial data profile and save to data/raw/data_profile.txt
    
    Include:
    - Number of rows and columns
    - Column names and types
    - Memory usage
    - First few rows preview
    """
    if df is None:
        df = load_raw_data()
        
    profile_path = 'data/raw/data_profile.txt'
    with open(profile_path, 'w') as f:
        f.write(f"Number of rows: {len(df)}\n")
        f.write(f"Number of columns: {len(df.columns)}\n")
        f.write(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")
        f.write("\nColumns and Types:\n")
        for col, dtype in df.dtypes.items():
            f.write(f"- {col}: {dtype}\n")
            
        f.write("\nFirst few rows:\n")
        f.write(df.head().to_string())
        
    print(f"Data profile generated at {profile_path}")

if __name__ == "__main__":
    download_dataset()
    df = load_raw_data()
    generate_data_profile(df)
