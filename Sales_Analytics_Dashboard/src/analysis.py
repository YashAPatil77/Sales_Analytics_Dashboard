"""
Analysis Module for Sales Analytics Dashboard (Indian Sales Dataset).

Computes key metrics, KPI benchmarks, regional/product/customer breakdowns,
and automatically generates data-driven business insights in Indian Rupees (₹).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

def compute_executive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes top-level executive KPIs.
    """
    if df.empty:
        return {
            'total_sales': 0.0,
            'total_profit': 0.0,
            'total_orders': 0,
            'total_quantity': 0,
            'avg_order_value': 0.0,
            'profit_margin_pct': 0.0,
            'sales_yoy_growth': 0.0,
            'profit_yoy_growth': 0.0
        }

    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    total_orders = int(df['Order ID'].nunique())
    total_quantity = int(df['Quantity'].sum())
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    profit_margin_pct = (total_profit / total_sales * 100.0) if total_sales > 0 else 0.0

    sales_yoy_growth = 0.0
    profit_yoy_growth = 0.0
    if 'Year' in df.columns:
        yearly = df.groupby('Year').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).sort_index()
        
        if len(yearly) >= 2:
            latest_year = yearly.index[-1]
            prev_year = yearly.index[-2]
            
            latest_sales = yearly.loc[latest_year, 'Sales']
            prev_sales = yearly.loc[prev_year, 'Sales']
            if prev_sales > 0:
                sales_yoy_growth = ((latest_sales - prev_sales) / prev_sales) * 100.0
                
            latest_profit = yearly.loc[latest_year, 'Profit']
            prev_profit = yearly.loc[prev_year, 'Profit']
            if abs(prev_profit) > 0:
                profit_yoy_growth = ((latest_profit - prev_profit) / abs(prev_profit)) * 100.0

    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_orders': total_orders,
        'total_quantity': total_quantity,
        'avg_order_value': avg_order_value,
        'profit_margin_pct': profit_margin_pct,
        'sales_yoy_growth': sales_yoy_growth,
        'profit_yoy_growth': profit_yoy_growth
    }

def get_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes Sales, Profit, Profit Margin %, Quantity, and Order Count by Category & Sub-Category.
    """
    cat_summary = df.groupby(['Category', 'Sub-Category']).agg(
        TotalSales=('Sales', 'sum'),
        TotalProfit=('Profit', 'sum'),
        TotalQuantity=('Quantity', 'sum'),
        TotalOrders=('Order ID', 'nunique'),
        AvgDiscount=('Discount', 'mean')
    ).reset_index()

    cat_summary['Profit Margin %'] = np.where(
        cat_summary['TotalSales'] > 0,
        (cat_summary['TotalProfit'] / cat_summary['TotalSales']) * 100.0,
        0.0
    )
    cat_summary['Avg Discount %'] = cat_summary['AvgDiscount'] * 100.0
    return cat_summary.sort_values(by='TotalSales', ascending=False)

def get_regional_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes Sales, Profit, Margin % by Region and State.
    """
    reg_summary = df.groupby(['Region', 'State']).agg(
        TotalSales=('Sales', 'sum'),
        TotalProfit=('Profit', 'sum'),
        TotalOrders=('Order ID', 'nunique'),
        TotalQuantity=('Quantity', 'sum')
    ).reset_index()

    reg_summary['Profit Margin %'] = np.where(
        reg_summary['TotalSales'] > 0,
        (reg_summary['TotalProfit'] / reg_summary['TotalSales']) * 100.0,
        0.0
    )
    return reg_summary.sort_values(by='TotalSales', ascending=False)

def get_top_bottom_products(df: pd.DataFrame, top_n: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns Top N products by Revenue and Bottom N products by Profitability (Loss-making).
    """
    prod_summary = df.groupby(['Product ID', 'Product Name', 'Category', 'Sub-Category']).agg(
        TotalSales=('Sales', 'sum'),
        TotalProfit=('Profit', 'sum'),
        TotalQuantity=('Quantity', 'sum'),
        AvgDiscount=('Discount', 'mean')
    ).reset_index()

    prod_summary['Profit Margin %'] = np.where(
        prod_summary['TotalSales'] > 0,
        (prod_summary['TotalProfit'] / prod_summary['TotalSales']) * 100.0,
        0.0
    )

    top_revenue = prod_summary.sort_values(by='TotalSales', ascending=False).head(top_n)
    bottom_profit = prod_summary.sort_values(by='TotalProfit', ascending=True).head(top_n)

    return top_revenue, bottom_profit

def get_discount_impact_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes how different discount brackets impact Profit Margin %.
    """
    disc_summary = df.groupby('Discount Level').agg(
        TotalSales=('Sales', 'sum'),
        TotalProfit=('Profit', 'sum'),
        OrderCount=('Order ID', 'nunique'),
        AvgDiscount=('Discount', 'mean'),
        LossCount=('Profit', lambda x: (x < 0).sum())
    ).reset_index()

    disc_summary['Profit Margin %'] = np.where(
        disc_summary['TotalSales'] > 0,
        (disc_summary['TotalProfit'] / disc_summary['TotalSales']) * 100.0,
        0.0
    )
    disc_summary['Loss Rate %'] = (disc_summary['LossCount'] / disc_summary['OrderCount']) * 100.0
    return disc_summary

def generate_automated_insights(df: pd.DataFrame) -> Dict[str, str]:
    """
    Dynamically generates executive analytical insights directly from dataset facts in INR (₹).
    """
    kpis = compute_executive_kpis(df)
    
    cat_df = df.groupby('Category').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
    top_sales_cat = cat_df.sort_values(by='Sales', ascending=False).iloc[0]
    top_profit_cat = cat_df.sort_values(by='Profit', ascending=False).iloc[0]

    sub_df = df.groupby('Sub-Category').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
    worst_subcat = sub_df.sort_values(by='Profit', ascending=True).iloc[0]

    reg_df = df.groupby('Region').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
    top_region = reg_df.sort_values(by='Sales', ascending=False).iloc[0]

    high_disc = df[df['Discount'] > 0.20]
    high_disc_profit = high_disc['Profit'].sum()
    high_disc_loss_pct = (high_disc['Profit'] < 0).mean() * 100.0 if len(high_disc) > 0 else 0.0

    insights = {
        'top_category': f"**{top_sales_cat['Category']}** leads all product categories with total sales of **₹{top_sales_cat['Sales']:,.2f}**.",
        'most_profitable_category': f"**{top_profit_cat['Category']}** generates the highest net profit (**₹{top_profit_cat['Profit']:,.2f}**).",
        'worst_sub_category': f"**{worst_subcat['Sub-Category']}** is severely underperforming with a total loss of **₹{worst_subcat['Profit']:,.2f}**.",
        'top_region': f"The **{top_region['Region']}** region is the top Indian territory with **₹{top_region['Sales']:,.2f}** in revenue and **₹{top_region['Profit']:,.2f}** in net profit.",
        'discount_warning': f"Orders with **discounts > 20%** experience a **{high_disc_loss_pct:.1f}% loss rate**, generating a cumulative loss of **₹{high_disc_profit:,.2f}**."
    }

    return insights
