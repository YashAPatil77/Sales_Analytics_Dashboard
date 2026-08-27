"""
Page 3: Profitability & Discount Analysis Component (Indian Sales Dataset).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

try:
    from src.analysis import get_discount_impact_analysis, get_top_bottom_products
    from src.visualization import plot_discount_vs_profit, plot_loss_products_bar, PALETTE
except ModuleNotFoundError:
    from Sales_Analytics_Dashboard.src.analysis import get_discount_impact_analysis, get_top_bottom_products
    from Sales_Analytics_Dashboard.src.visualization import plot_discount_vs_profit, plot_loss_products_bar, PALETTE

def render_profitability_page(df: pd.DataFrame):
    st.markdown("## 💸 Profitability & Discount Destruction Analysis")
    st.markdown("Deep dive into profit margins, loss-making products, and margin erosion in Indian Rupees (₹).")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 📉 Discount Rate vs. Net Profit (₹ INR)")
        fig_disc = plot_discount_vs_profit(df)
        st.plotly_chart(fig_disc, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("### 📊 Margin Degradation by Discount Level")
        disc_summary = get_discount_impact_analysis(df)
        
        st.dataframe(
            disc_summary[['Discount Level', 'TotalSales', 'TotalProfit', 'Profit Margin %', 'Loss Rate %']].style.format({
                'TotalSales': '₹{:,.2f}',
                'TotalProfit': '₹{:,.2f}',
                'Profit Margin %': '{:.1f}%',
                'Loss Rate %': '{:.1f}%'
            }),
            use_container_width=True
        )

        st.warning(
            "💡 **Critical Insight**: Products sold with **discounts > 20%** severely erode overall profitability. "
            "Enforcing a maximum 15% discount cap will instantly eliminate corporate margin loss."
        )

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🚫 Top 10 Loss-Making Products")
        _, bottom_profit = get_top_bottom_products(df, top_n=10)
        fig_loss = plot_loss_products_bar(bottom_profit)
        st.plotly_chart(fig_loss, use_container_width=True, config={'displayModeBar': False})

    with col4:
        st.markdown("### 📉 Sub-Category Profit Margins")
        sub_profit = df.groupby('Sub-Category').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).reset_index()
        sub_profit['Margin %'] = (sub_profit['Profit'] / sub_profit['Sales']) * 100.0
        sub_profit = sub_profit.sort_values(by='Margin %', ascending=True)

        fig_sub_m = px.bar(
            sub_profit,
            x='Margin %',
            y='Sub-Category',
            orientation='h',
            color='Margin %',
            color_continuous_scale="RdYlGn",
            text=[f"{x:.1f}%" for x in sub_profit['Margin %']]
        )
        fig_sub_m.update_layout(template="plotly_dark", title=None, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20))
        st.plotly_chart(fig_sub_m, use_container_width=True, config={'displayModeBar': False})
