"""
Feature Engineering Module for Sales Analytics Dashboard.

Creates derived metrics, financial KPIs, customer RFM features,
time components, and profitability categories.
"""

import pandas as pd
import numpy as np

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts temporal components from Order Date.
    """
    data = df.copy()
    if 'Order Date' not in data.columns or not pd.api.types.is_datetime64_any_dtype(data['Order Date']):
        data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')

    data['Year'] = data['Order Date'].dt.year
    data['Month'] = data['Order Date'].dt.month
    data['Month Name'] = data['Order Date'].dt.strftime('%b')
    data['Quarter'] = 'Q' + data['Order Date'].dt.quarter.astype(str)
    data['Day of Week'] = data['Order Date'].dt.day_name()
    data['Year-Month'] = data['Order Date'].dt.strftime('%Y-%m')
    data['Year-Quarter'] = data['Year'].astype(str) + '-' + data['Quarter']
    return data

def add_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds derived financial metrics:
    - Profit Margin %
    - Unit Price
    - Total Cost
    - Profitability Category
    - Discount Category
    """
    data = df.copy()
    
    # Safe division for Profit Margin %
    data['Profit Margin %'] = np.where(
        data['Sales'] > 0,
        (data['Profit'] / data['Sales']) * 100.0,
        0.0
    )
    
    # Unit Price & Total Cost
    data['Unit Price'] = np.where(
        data['Quantity'] > 0,
        data['Sales'] / data['Quantity'],
        data['Sales']
    )
    data['Cost'] = data['Sales'] - data['Profit']
    data['Cost per Unit'] = np.where(
        data['Quantity'] > 0,
        data['Cost'] / data['Quantity'],
        data['Cost']
    )

    # Profitability Status Category
    conditions_profit = [
        (data['Profit Margin %'] > 20.0),
        (data['Profit Margin %'] >= 0.0) & (data['Profit Margin %'] <= 20.0),
        (data['Profit Margin %'] < 0.0)
    ]
    choices_profit = ['High Margin (>20%)', 'Moderate Margin (0-20%)', 'Loss-Making (<0%)']
    data['Profitability Category'] = np.select(conditions_profit, choices_profit, default='Moderate Margin (0-20%)')

    # Discount Level Category
    conditions_disc = [
        (data['Discount'] == 0.0),
        (data['Discount'] > 0.0) & (data['Discount'] <= 0.20),
        (data['Discount'] > 0.20)
    ]
    choices_disc = ['No Discount (0%)', 'Moderate Discount (1-20%)', 'High Discount (>20%)']
    data['Discount Level'] = np.select(conditions_disc, choices_disc, default='No Discount (0%)')

    return data

def compute_customer_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes RFM (Recency, Frequency, Monetary) metrics per Customer.
    Returns DataFrame indexed by Customer ID / Customer Name.
    """
    if 'Customer ID' not in df.columns or 'Order Date' not in df.columns:
        return pd.DataFrame()

    snapshot_date = df['Order Date'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby(['Customer ID', 'Customer Name', 'Segment']).agg(
        Recency=('Order Date', lambda x: (snapshot_date - x.max()).days),
        Frequency=('Order ID', 'nunique'),
        Monetary=('Sales', 'sum'),
        TotalProfit=('Profit', 'sum'),
        AvgOrderValue=('Sales', lambda x: x.sum() / max(1, x.nunique()))
    ).reset_index()

    # Assign R, F, M quartiles (1 to 4)
    rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop').astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=4, labels=[1, 2, 3, 4], duplicates='drop').astype(int)
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

    # Define RFM Customer Tiers
    def segment_rfm(row):
        score = row['R_Score'] + row['F_Score'] + row['M_Score']
        if score >= 10:
            return 'Champions'
        elif score >= 8:
            return 'Loyal Customers'
        elif score >= 6:
            return 'Potential Customers'
        elif score >= 4:
            return 'At Risk'
        else:
            return 'Lost Customers'

    rfm['Customer Tier'] = rfm.apply(segment_rfm, axis=1)
    return rfm

def compute_pareto_analysis(df: pd.DataFrame, group_col: str = 'Product Name') -> pd.DataFrame:
    """
    Computes Pareto 80/20 cumulative sales breakdown for products or sub-categories.
    """
    pareto_df = df.groupby(group_col).agg(
        TotalSales=('Sales', 'sum'),
        TotalProfit=('Profit', 'sum'),
        TotalQuantity=('Quantity', 'sum')
    ).sort_values(by='TotalSales', ascending=False).reset_index()

    pareto_df['CumulativeSales'] = pareto_df['TotalSales'].cumsum()
    grand_sales = pareto_df['TotalSales'].sum()
    pareto_df['CumulativePct'] = (pareto_df['CumulativeSales'] / grand_sales) * 100.0
    pareto_df['Pareto Class'] = np.where(pareto_df['CumulativePct'] <= 80.0, 'Top 80% Revenue Drivers', 'Bottom 20% Tail')
    
    return pareto_df

def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies complete feature engineering pipeline to cleaned DataFrame.
    """
    data = add_time_features(df)
    data = add_financial_metrics(data)
    print(f"[FEATURE ENGINEERING] Created derived time & financial metrics. Total columns: {len(data.columns)}")
    return data
