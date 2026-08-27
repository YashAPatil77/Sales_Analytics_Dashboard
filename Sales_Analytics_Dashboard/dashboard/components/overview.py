"""
Page 1: Executive Overview Component (Indian Sales Dataset).
"""

import streamlit as st
import pandas as pd

try:
    from src.analysis import compute_executive_kpis, get_category_performance, generate_automated_insights
    from src.forecasting import prepare_monthly_timeseries
    from src.visualization import plot_sales_profit_trend, plot_category_sales_profit
except ModuleNotFoundError:
    from Sales_Analytics_Dashboard.src.analysis import compute_executive_kpis, get_category_performance, generate_automated_insights
    from Sales_Analytics_Dashboard.src.forecasting import prepare_monthly_timeseries
    from Sales_Analytics_Dashboard.src.visualization import plot_sales_profit_trend, plot_category_sales_profit

def format_inr(val: float) -> str:
    """Formats large INR currency values into clean Lakhs/Crores notation."""
    if abs(val) >= 10_000_000:
        return f"₹{val / 10_000_000:,.2f} Cr"
    elif abs(val) >= 100_000:
        return f"₹{val / 100_000:,.2f} L"
    else:
        return f"₹{val:,.2f}"

def render_overview_page(df: pd.DataFrame):
    st.markdown("## 📊 Executive Overview (India Market)")
    st.markdown("High-level executive KPIs, top-line performance metrics, and category revenue breakdowns in Indian Rupees (₹).")

    # 1. Executive KPI Cards
    kpis = compute_executive_kpis(df)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Sales",
            value=format_inr(kpis['total_sales']),
            delta=f"{kpis['sales_yoy_growth']:+.1f}% YoY" if kpis['sales_yoy_growth'] else None,
            help=f"Full Sales Amount: ₹{kpis['total_sales']:,.2f}"
        )

    with col2:
        st.metric(
            label="Total Profit",
            value=format_inr(kpis['total_profit']),
            delta=f"{kpis['profit_yoy_growth']:+.1f}% YoY" if kpis['profit_yoy_growth'] else None,
            help=f"Full Profit Amount: ₹{kpis['total_profit']:,.2f}"
        )

    with col3:
        st.metric(
            label="Total Orders",
            value=f"{kpis['total_orders']:,}"
        )

    with col4:
        st.metric(
            label="Avg Order Value (AOV)",
            value=f"₹{kpis['avg_order_value']:,.2f}"
        )

    with col5:
        st.metric(
            label="Profit Margin",
            value=f"{kpis['profit_margin_pct']:.1f}%"
        )

    st.markdown("---")

    # 2. Main Visualizations Grid
    row1_col1, row1_col2 = st.columns([3, 2])

    with row1_col1:
        st.markdown("### 📈 Monthly Revenue & Profit Trends")
        monthly_df = prepare_monthly_timeseries(df)
        fig_trend = plot_sales_profit_trend(monthly_df)
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})

    with row1_col2:
        st.markdown("### 🏷️ Category Sales & Profit Performance")
        cat_df = get_category_performance(df)
        fig_cat = plot_category_sales_profit(cat_df)
        st.plotly_chart(fig_cat, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # 3. Dynamic Executive Insights
    st.markdown("### 💡 Key Business Takeaways")
    insights = generate_automated_insights(df)

    ins_col1, ins_col2 = st.columns(2)
    with ins_col1:
        st.info(f"🏆 **Revenue Leader**: {insights['top_category']}")
        st.success(f"💰 **Profit Leader**: {insights['most_profitable_category']}")
        st.warning(f"📍 **Top Territory**: {insights['top_region']}")

    with ins_col2:
        st.error(f"⚠️ **Loss-Making Category**: {insights['worst_sub_category']}")
        st.error(f"🚨 **Discount Danger**: {insights['discount_warning']}")
