"""
Page 2: Sales & Regional Analysis Component (Indian Sales Dataset).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

try:
    from src.analysis import get_regional_performance, get_category_performance
    from src.visualization import plot_state_performance, PALETTE
except ModuleNotFoundError:
    from Sales_Analytics_Dashboard.src.analysis import get_regional_performance, get_category_performance
    from Sales_Analytics_Dashboard.src.visualization import plot_state_performance, PALETTE

def render_sales_analysis_page(df: pd.DataFrame):
    st.markdown("## 🇮🇳 Regional & Indian State Sales Performance")
    st.markdown("Geographical revenue distribution across Indian states, cities, territories, and courier logistics modes.")

    reg_df = get_regional_performance(df)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("### 🗺️ Revenue by Indian State")
        fig_map = plot_state_performance(reg_df)
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("### 🏆 Top Performing Indian States")
        top_states = reg_df.groupby('State').agg(
            Sales=('TotalSales', 'sum'),
            Profit=('TotalProfit', 'sum'),
            Margin=('Profit Margin %', 'mean')
        ).sort_values(by='Sales', ascending=False).head(10).reset_index()

        st.dataframe(
            top_states.style.format({
                'Sales': '₹{:,.2f}',
                'Profit': '₹{:,.2f}',
                'Margin': '{:.1f}%'
            }),
            use_container_width=True
        )

    st.markdown("---")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("### 🚚 Revenue by Courier Logistics Mode")
        ship_df = df.groupby('Ship Mode').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            AvgDays=('Shipping Days', 'mean')
        ).reset_index()

        fig_ship = px.bar(
            ship_df,
            x='Ship Mode',
            y='Sales',
            color='Ship Mode',
            text=[f"₹{x:,.0f}" for x in ship_df['Sales']],
            color_discrete_sequence=PALETTE
        )
        fig_ship.update_layout(template="plotly_dark", title=None, showlegend=False, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20))
        st.plotly_chart(fig_ship, use_container_width=True, config={'displayModeBar': False})

    with row2_col2:
        st.markdown("### 🏷️ Sub-Category Revenue Ranking")
        sub_df = get_category_performance(df).sort_values(by='TotalSales', ascending=True)
        fig_sub = px.bar(
            sub_df,
            x='TotalSales',
            y='Sub-Category',
            orientation='h',
            color='Category',
            color_discrete_sequence=PALETTE,
            text=[f"₹{x:,.0f}" for x in sub_df['TotalSales']]
        )
        fig_sub.update_layout(template="plotly_dark", title=None, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20), legend=dict(title_text="", orientation="h", y=1.05))
        st.plotly_chart(fig_sub, use_container_width=True, config={'displayModeBar': False})
