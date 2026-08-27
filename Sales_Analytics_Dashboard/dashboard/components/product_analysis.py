"""
Page 4: Product & Customer Intelligence Component (Indian Sales Dataset).
"""

import streamlit as st
import pandas as pd

try:
    from src.analysis import get_top_bottom_products
    from src.feature_engineering import compute_customer_rfm, compute_pareto_analysis
    from src.visualization import plot_top_products_bar, plot_rfm_segments_donut
except ModuleNotFoundError:
    from Sales_Analytics_Dashboard.src.analysis import get_top_bottom_products
    from Sales_Analytics_Dashboard.src.feature_engineering import compute_customer_rfm, compute_pareto_analysis
    from Sales_Analytics_Dashboard.src.visualization import plot_top_products_bar, plot_rfm_segments_donut

def render_product_analysis_page(df: pd.DataFrame):
    st.markdown("## 📦 Product & Indian Customer Intelligence")
    st.markdown("Product performance, Pareto 80/20 revenue concentration, and Customer RFM segmentation.")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🏆 Top 10 Revenue Products")
        top_revenue, _ = get_top_bottom_products(df, top_n=10)
        fig_top = plot_top_products_bar(top_revenue)
        st.plotly_chart(fig_top, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("### 🎯 Pareto 80/20 Analysis")
        pareto_df = compute_pareto_analysis(df, group_col='Sub-Category')
        top_80 = pareto_df[pareto_df['Pareto Class'] == 'Top 80% Revenue Drivers']
        
        st.write(f"**{len(top_80)} out of {len(pareto_df)} Sub-Categories** generate **80% of total Indian revenue**:")
        st.dataframe(
            pareto_df[['Sub-Category', 'TotalSales', 'CumulativePct', 'Pareto Class']].style.format({
                'TotalSales': '₹{:,.2f}',
                'CumulativePct': '{:.1f}%'
            }),
            use_container_width=True
        )

    st.markdown("---")

    col3, col4 = st.columns([2, 3])

    with col3:
        st.markdown("### 👥 Customer RFM Segments")
        rfm_df = compute_customer_rfm(df)
        if not rfm_df.empty:
            fig_rfm = plot_rfm_segments_donut(rfm_df)
            st.plotly_chart(fig_rfm, use_container_width=True, config={'displayModeBar': False})

    with col4:
        st.markdown("### 👑 Top 10 High-Value Indian Customers")
        if not rfm_df.empty:
            top_cust = rfm_df.sort_values(by='Monetary', ascending=False).head(10)
            st.dataframe(
                top_cust[['Customer Name', 'Segment', 'Monetary', 'Frequency', 'Recency', 'Customer Tier']].style.format({
                    'Monetary': '₹{:,.2f}',
                    'Recency': '{:,} days'
                }),
                use_container_width=True
            )
