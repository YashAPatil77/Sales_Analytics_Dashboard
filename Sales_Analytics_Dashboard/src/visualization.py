"""
Visualization Module for Sales Analytics Dashboard (Indian Sales Dataset).

Provides high-aesthetic Plotly chart generators, theme-adaptive formatting,
and custom KPI cards using Indian Rupees (₹).
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any

# Custom Color Palette
COLOR_PRIMARY = "#3B82F6"      # Bright Accent Blue
COLOR_SUCCESS = "#10B981"      # Emerald Green
COLOR_WARNING = "#F59E0B"      # Amber Orange
COLOR_DANGER = "#EF4444"       # Coral Red
COLOR_PURPLE = "#8B5CF6"       # Electric Violet

PALETTE = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6", "#F97316"]

def apply_chart_theme(fig: go.Figure) -> go.Figure:
    """
    Applies custom theme-adaptive styling to Plotly figures.
    Uses transparent background so charts adapt seamlessly to both Light & Dark modes.
    """
    fig.layout.title = None # Completely remove internal title object
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0.05)",
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=30, r=30, t=15, b=35),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            title_text="",
            bgcolor="rgba(128, 128, 128, 0.15)",
            bordercolor="rgba(128, 128, 128, 0.3)",
            borderwidth=1,
            font=dict(size=11)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",
            zeroline=False
        )
    )
    return fig

def plot_sales_profit_trend(monthly_df: pd.DataFrame) -> go.Figure:
    """
    Creates monthly Sales (₹) and Profit (₹) dual line chart.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly_df['Order Date'],
        y=monthly_df['Sales'],
        name='Total Sales (₹)',
        mode='lines+markers',
        line=dict(color=COLOR_PRIMARY, width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.15)',
        hovertemplate="<b>Date:</b> %{x|%b %Y}<br><b>Sales:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=monthly_df['Order Date'],
        y=monthly_df['Profit'],
        name='Total Profit (₹)',
        mode='lines+markers',
        line=dict(color=COLOR_SUCCESS, width=3, shape='spline'),
        hovertemplate="<b>Date:</b> %{x|%b %Y}<br><b>Profit:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    return apply_chart_theme(fig)

def plot_category_sales_profit(cat_df: pd.DataFrame) -> go.Figure:
    """
    Creates grouped bar chart for Sales & Profit by Category (₹).
    """
    summary = cat_df.groupby('Category').agg(
        Sales=('TotalSales', 'sum'),
        Profit=('TotalProfit', 'sum')
    ).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=summary['Category'],
        y=summary['Sales'],
        name='Sales (₹)',
        marker_color=COLOR_PRIMARY,
        text=[f"₹{x:,.0f}" for x in summary['Sales']],
        textposition='auto',
        hovertemplate="<b>Category:</b> %{x}<br><b>Sales:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=summary['Category'],
        y=summary['Profit'],
        name='Profit (₹)',
        marker_color=COLOR_SUCCESS,
        text=[f"₹{x:,.0f}" for x in summary['Profit']],
        textposition='auto',
        hovertemplate="<b>Category:</b> %{x}<br><b>Profit:</b> ₹%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(barmode='group')
    return apply_chart_theme(fig)

def plot_state_performance(reg_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart ranking Indian States by Total Sales & Profit.
    """
    state_summary = reg_df.groupby('State').agg(
        Sales=('TotalSales', 'sum'),
        Profit=('TotalProfit', 'sum')
    ).sort_values(by='Sales', ascending=True).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=state_summary['Sales'],
        y=state_summary['State'],
        orientation='h',
        name='Sales (₹)',
        marker_color=COLOR_PRIMARY,
        text=[f"₹{x:,.0f}" for x in state_summary['Sales']],
        textposition='outside',
        hovertemplate="<b>State:</b> %{y}<br><b>Sales:</b> ₹%{x:,.2f}<extra></extra>"
    ))

    return apply_chart_theme(fig)

def plot_discount_vs_profit(df: pd.DataFrame) -> go.Figure:
    """
    Creates scatter plot with OLS trendline demonstrating discount impact on profitability in INR.
    """
    sample_df = df.sample(min(1500, len(df)), random_state=42) if len(df) > 1500 else df

    fig = px.scatter(
        sample_df,
        x='Discount',
        y='Profit',
        color='Category',
        size='Sales',
        hover_data=['Sub-Category', 'State'],
        color_discrete_sequence=PALETTE,
        trendline="ols",
        opacity=0.75
    )

    fig.update_xaxes(tickformat=".0%")
    fig = apply_chart_theme(fig)
    return fig

def plot_top_products_bar(top_revenue: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart for Top 10 Revenue Products (₹).
    """
    top_revenue_sorted = top_revenue.sort_values(by='TotalSales', ascending=True)

    fig = go.Figure(go.Bar(
        x=top_revenue_sorted['TotalSales'],
        y=top_revenue_sorted['Product Name'].str.slice(0, 35),
        orientation='h',
        marker=dict(
            color=top_revenue_sorted['TotalSales'],
            colorscale='Viridis'
        ),
        text=[f"₹{x:,.0f}" for x in top_revenue_sorted['TotalSales']],
        textposition='outside',
        hovertemplate="<b>Product:</b> %{y}<br><b>Sales:</b> ₹%{x:,.2f}<extra></extra>"
    ))

    return apply_chart_theme(fig)

def plot_loss_products_bar(bottom_profit: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart for Loss-Making Products (₹).
    """
    bottom_sorted = bottom_profit.sort_values(by='TotalProfit', ascending=False)

    fig = go.Figure(go.Bar(
        x=bottom_sorted['TotalProfit'],
        y=bottom_sorted['Product Name'].str.slice(0, 35),
        orientation='h',
        marker_color=COLOR_DANGER,
        text=[f"₹{x:,.0f}" for x in bottom_sorted['TotalProfit']],
        textposition='outside',
        hovertemplate="<b>Product:</b> %{y}<br><b>Profit:</b> ₹%{x:,.2f}<extra></extra>"
    ))

    return apply_chart_theme(fig)

def plot_rfm_segments_donut(rfm_df: pd.DataFrame) -> go.Figure:
    """
    Donut chart of Customer Segment Tiers with clean text alignment and horizontal legend below.
    """
    tier_counts = rfm_df['Customer Tier'].value_counts().reset_index()
    tier_counts.columns = ['Customer Tier', 'Count']

    fig = px.pie(
        tier_counts,
        names='Customer Tier',
        values='Count',
        hole=0.55,
        color_discrete_sequence=PALETTE
    )

    fig.update_traces(
        textinfo='percent+label',
        insidetextorientation='horizontal',
        marker=dict(line=dict(width=2))
    )
    
    fig = apply_chart_theme(fig)
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=40),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
            title_text="",
            bgcolor="rgba(128, 128, 128, 0.15)",
            bordercolor="rgba(128, 128, 128, 0.3)",
            borderwidth=1,
            font=dict(size=11)
        )
    )
    return fig

def plot_forecast_chart(combined_df: pd.DataFrame) -> go.Figure:
    """
    Creates sales forecast chart in INR (₹).
    """
    fig = go.Figure()

    hist_data = combined_df[combined_df['Type'] == 'Actual Historical']
    fc_data = combined_df[combined_df['Type'] == 'Forecast']

    # Historical Line
    fig.add_trace(go.Scatter(
        x=hist_data['Date'],
        y=hist_data['Sales'],
        name='Historical Sales (₹)',
        mode='lines+markers',
        line=dict(color=COLOR_PRIMARY, width=3)
    ))

    # Upper Bound
    fig.add_trace(go.Scatter(
        x=fc_data['Date'],
        y=fc_data['Upper Bound'],
        name='Upper 95% CI',
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))

    # Lower Bound
    fig.add_trace(go.Scatter(
        x=fc_data['Date'],
        y=fc_data['Lower Bound'],
        name='95% Confidence Interval',
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(139, 92, 246, 0.25)'
    ))

    # Forecast Line
    fig.add_trace(go.Scatter(
        x=fc_data['Date'],
        y=fc_data['Sales'],
        name='6-Month Forecast (₹)',
        mode='lines+markers',
        line=dict(color=COLOR_PURPLE, width=3, dash='dash')
    ))

    return apply_chart_theme(fig)
