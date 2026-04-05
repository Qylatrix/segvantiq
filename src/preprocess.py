import pandas as pd
import datetime as dt
import os

from typing import Tuple

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Loads raw customer transaction dataset and cleans anomalies.
    """
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    
    # 1. Handle missing CustomerIDs. Without them, we cannot cluster customers.
    initial_rows = len(df)
    df.dropna(subset=['CustomerID'], inplace=True)
    print(f"Removed {initial_rows - len(df)} rows with missing CustomerID.")
    
    # 2. Convert InvoiceDate to datetime objects
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # 3. Handle anomalies: remove negative quantities (returns/cancellations)
    df = df[df['Quantity'] > 0]
    
    # 4. Handle anomalies: remove zero or negative unit prices
    df = df[df['UnitPrice'] > 0]
    
    print(f"Data cleaned. Proceeding with {len(df)} valid transaction rows.")
    return df

def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms transactional data into Recency, Frequency, and Monetary value metrics per customer.
    """
    print("Calculating RFM (Recency, Frequency, Monetary) metrics...")
    
    # Calculate Total Price per row
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    # Define a 'current' date as 1 day after the max date in the dataset to calculate recency
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    
    # Aggregate data at the CustomerID level
    rfm = df.groupby('CustomerID').agg(
        Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
        Tenure=('InvoiceDate', lambda x: (snapshot_date - x.min()).days),
        Frequency=('InvoiceNo', 'nunique'),
        Monetary=('TotalPrice', 'sum')
    ).reset_index()
    
    print(f"RFM built successfully for {len(rfm)} unique customers.")
    return rfm

def preprocess_pipeline() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Helper pipeline to load, clean, and run feature engineering continuously for the app.
    If no dataset is found, auto-generates a synthetic demo dataset so the app works
    on Streamlit Community Cloud without manual data setup.
    """
    input_file = "data/customer_data.csv"
    if not os.path.exists(input_file):
        # Auto-generate demo data — this makes the live deployment self-contained
        from src.data_generator import generate_demo_dataset
        print("[preprocess] No data found — generating synthetic demo dataset...")
        generate_demo_dataset(n_customers=800, output_path=input_file)

    df_clean = load_and_clean_data(input_file)
    df_rfm = calculate_rfm(df_clean)

    return df_clean, df_rfm

if __name__ == "__main__":
    # Ensure data output directory exists
    os.makedirs('data', exist_ok=True)
    
    input_file = "data/customer_data.csv"
    output_file = "data/rfm_data.csv"
    
    if not os.path.exists(input_file):
        print(f"Could not find {input_file}. Please ensure raw data is placed there.")
        exit(1)
        
    cleaned_df = load_and_clean_data(input_file)
    rfm_df = calculate_rfm(cleaned_df)
    
    # Save the feature engineered data
    rfm_df.to_csv(output_file, index=False)
    print(f"Feature-engineered RFM dataset saved to {output_file}")
