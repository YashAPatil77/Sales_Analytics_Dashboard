"""
Data Cleaning Module for Sales Analytics Dashboard.

Provides robust functions to read, clean, format, and validate
the Kaggle Superstore Sales dataset.
"""

import os
import pandas as pd
import numpy as np

def load_raw_data(filepath: str = "data/raw/sample_superstore.csv") -> pd.DataFrame:
    """
    Loads raw CSV sales dataset with multi-encoding fallback support.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")
    
    encodings = ['windows-1252', 'latin1', 'utf-8', 'cp1252']
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            print(f"[DATA CLEANING] Successfully loaded raw data with encoding '{enc}'. Shape: {df.shape}")
            break
        except Exception:
            continue
            
    if df is None:
        raise ValueError(f"Failed to read dataset from {filepath} with any supported encoding.")
        
    return df

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw sales dataset:
    - Parses date columns (Order Date, Ship Date)
    - Strips whitespace from string columns
    - Calculates Shipping Duration (Days)
    - Validates numerical integrity (Sales, Quantity, Profit, Discount)
    - Handles missing values cleanly
    """
    cleaned_df = df.copy()
    
    # Clean column names (strip space)
    cleaned_df.columns = cleaned_df.columns.str.strip()
    
    # Strip string fields
    string_cols = cleaned_df.select_dtypes(include=['object', 'string']).columns
    for col in string_cols:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        
    # Convert dates
    date_cols = ['Order Date', 'Ship Date']
    for col in date_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            
    # Calculate Shipping Duration
    if 'Order Date' in cleaned_df.columns and 'Ship Date' in cleaned_df.columns:
        cleaned_df['Shipping Days'] = (cleaned_df['Ship Date'] - cleaned_df['Order Date']).dt.days
        # Fill any invalid negative shipping days with 0
        cleaned_df['Shipping Days'] = cleaned_df['Shipping Days'].apply(lambda x: max(0, x) if pd.notnull(x) else 0)

    # Convert numeric fields
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    for col in numeric_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0.0)

    # Validate non-negative quantities and sales
    cleaned_df['Sales'] = cleaned_df['Sales'].clip(lower=0.0)
    cleaned_df['Quantity'] = cleaned_df['Quantity'].clip(lower=1)
    cleaned_df['Discount'] = cleaned_df['Discount'].clip(lower=0.0, upper=1.0)
    
    # Fill Postal Code missing values with 'Unknown'
    if 'Postal Code' in cleaned_df.columns:
        cleaned_df['Postal Code'] = cleaned_df['Postal Code'].replace('nan', 'Unknown').fillna('Unknown')
        
    # Deduplicate exact duplicate rows if any
    initial_count = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates()
    dedup_count = len(cleaned_df)
    if initial_count != dedup_count:
        print(f"[DATA CLEANING] Dropped {initial_count - dedup_count} exact duplicate rows.")

    return cleaned_df

def save_processed_data(df: pd.DataFrame, output_path: str = "data/processed/sales_data_cleaned.csv") -> None:
    """
    Saves cleaned and processed DataFrame to CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[DATA CLEANING] Cleaned data saved successfully to: {output_path}")

if __name__ == "__main__":
    raw = load_raw_data()
    cleaned = clean_sales_data(raw)
    save_processed_data(cleaned)
