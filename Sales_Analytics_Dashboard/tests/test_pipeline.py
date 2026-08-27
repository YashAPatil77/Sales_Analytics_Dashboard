"""
Unit Tests for Sales Analytics Dashboard Data Pipeline (Indian Sales Dataset).
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_cleaning import load_raw_data, clean_sales_data
from src.feature_engineering import apply_feature_engineering
from src.analysis import compute_executive_kpis
from src.forecasting import prepare_monthly_timeseries, train_sales_forecast

@pytest.fixture
def sample_indian_raw_df():
    """
    Creates a sample raw dataframe fixture for Indian dataset.
    """
    return pd.DataFrame({
        'Order ID': ['B-25601', 'B-25602', 'B-25603'],
        'Order Date': ['2022-01-01', '2022-02-15', '2022-03-20'],
        'Ship Date': ['2022-01-05', '2022-02-18', '2022-03-25'],
        'Ship Mode': ['BlueDart Express', 'Standard Express', 'Same Day Delivery'],
        'Customer ID': ['IND-CUST-1001', 'IND-CUST-1002', 'IND-CUST-1003'],
        'Customer Name': ['Aarav Sharma', 'Priya Patel', 'Rajesh Kumar'],
        'Segment': ['Consumer', 'Corporate', 'Small Business'],
        'Country': ['India', 'India', 'India'],
        'City': ['Mumbai', 'Delhi', 'Bangalore'],
        'State': ['Maharashtra', 'Delhi', 'Karnataka'],
        'Postal Code': [400001, 110001, 560001],
        'Region': ['West', 'North', 'South'],
        'Product ID': ['IND-PRD-101', 'IND-PRD-102', 'IND-PRD-103'],
        'Category': ['Electronics', 'Clothing', 'Furniture'],
        'Sub-Category': ['Printers', 'Sarees', 'Tables'],
        'Product Name': ['Printers - Grade A', 'Sarees - Premium', 'Tables - Standard'],
        'Sales': [15000.0, 5000.0, 12000.0],
        'Quantity': [2, 3, 1],
        'Discount': [0.1, 0.0, 0.25],
        'Profit': [3000.0, 1200.0, -1500.0]
    })

def test_clean_sales_data(sample_indian_raw_df):
    cleaned = clean_sales_data(sample_indian_raw_df)
    assert len(cleaned) == 3
    assert pd.api.types.is_datetime64_any_dtype(cleaned['Order Date'])
    assert pd.api.types.is_datetime64_any_dtype(cleaned['Ship Date'])
    assert 'Shipping Days' in cleaned.columns
    assert (cleaned['Shipping Days'] >= 0).all()

def test_feature_engineering(sample_indian_raw_df):
    cleaned = clean_sales_data(sample_indian_raw_df)
    featured = apply_feature_engineering(cleaned)
    
    assert 'Profit Margin %' in featured.columns
    assert 'Year' in featured.columns
    assert 'Month' in featured.columns
    assert 'Profitability Category' in featured.columns
    
    # Verify Profit Margin % calculation: 3000/15000 * 100 = 20.0%
    assert abs(featured.loc[0, 'Profit Margin %'] - 20.0) < 1e-5
    assert featured.loc[2, 'Profitability Category'] == 'Loss-Making (<0%)'

def test_kpi_calculations(sample_indian_raw_df):
    cleaned = clean_sales_data(sample_indian_raw_df)
    featured = apply_feature_engineering(cleaned)
    kpis = compute_executive_kpis(featured)

    assert kpis['total_sales'] == 32000.0
    assert kpis['total_profit'] == 3000.0 + 1200.0 - 1500.0
    assert kpis['total_orders'] == 3
    assert kpis['total_quantity'] == 6
    assert abs(kpis['avg_order_value'] - (32000.0 / 3)) < 1e-5

def test_forecasting_pipeline(sample_indian_raw_df):
    cleaned = clean_sales_data(sample_indian_raw_df)
    featured = apply_feature_engineering(cleaned)
    monthly = prepare_monthly_timeseries(featured)
    
    assert not monthly.empty
    combined, metrics = train_sales_forecast(monthly, forecast_periods=3)
    assert not combined.empty
    assert 'Forecast' in combined['Type'].values
    assert 'MAE' in metrics
