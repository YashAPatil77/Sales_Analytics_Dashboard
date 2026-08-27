"""
Page 5: Advanced Forecasting & Scenario Modeling Component (Indian Sales Dataset).
"""

import streamlit as st
import pandas as pd
import numpy as np

try:
    from src.forecasting import prepare_monthly_timeseries, train_sales_forecast
    from src.visualization import plot_forecast_chart
except ModuleNotFoundError:
    from Sales_Analytics_Dashboard.src.forecasting import prepare_monthly_timeseries, train_sales_forecast
    from Sales_Analytics_Dashboard.src.visualization import plot_forecast_chart

def render_forecasting_page(df: pd.DataFrame):
    st.markdown("## 🔮 Advanced Predictive Forecasting & Scenario Simulator")
    st.markdown("Time-series monthly sales prediction in INR (₹) with 95% confidence intervals and interactive profit optimization scenario modeling.")

    # 1. Sales Forecasting
    monthly_df = prepare_monthly_timeseries(df)
    
    col_ctrl, col_chart = st.columns([1, 3])
    
    with col_ctrl:
        st.markdown("### ⚙️ Forecast Controls")
        forecast_months = st.slider("Forecast Horizon (Months)", min_value=3, max_value=12, value=6)
        
        combined_fc, metrics = train_sales_forecast(monthly_df, forecast_periods=forecast_months)
        
        st.markdown("#### 📐 Model Evaluation")
        st.metric("Mean Absolute Error (MAE)", f"₹{metrics['MAE']:,.2f}")
        st.metric("Root Mean Sq Error (RMSE)", f"₹{metrics['RMSE']:,.2f}")
        st.metric("Mean Abs Pct Error (MAPE)", f"{metrics['MAPE']:.1f}%")

    with col_chart:
        st.markdown("### 🔮 Indian Monthly Sales Forecast (₹ INR)")
        fig_fc = plot_forecast_chart(combined_fc)
        st.plotly_chart(fig_fc, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # 2. Interactive Scenario Simulator
    st.markdown("### 🧪 What-If Scenario Simulator: Discount Restriction Impact")
    st.markdown("Simulate how capping maximum product discounts recovers destroyed corporate profit in Indian Rupees (₹).")

    col_sim1, col_sim2 = st.columns([2, 3])

    with col_sim1:
        max_discount_cap = st.slider(
            "Select Maximum Allowed Discount Cap (%)",
            min_value=0,
            max_value=30,
            value=15,
            step=5
        ) / 100.0

        # Calculate simulated profit
        sim_df = df.copy()
        high_disc_mask = sim_df['Discount'] > max_discount_cap
        
        # Reset high discount to cap and recalculate profit
        sim_df.loc[high_disc_mask, 'Discount'] = max_discount_cap
        sim_df['New Sales'] = sim_df['Sales'] * (1 - sim_df['Discount']) / np.maximum(0.01, (1 - df['Discount']))
        sim_df['New Profit'] = sim_df['New Sales'] - sim_df['Cost']

        orig_total_profit = df['Profit'].sum()
        sim_total_profit = sim_df['New Profit'].sum()
        profit_recovery = sim_total_profit - orig_total_profit

        st.metric(
            label="Simulated Total Corporate Profit",
            value=f"₹{sim_total_profit:,.2f}",
            delta=f"+₹{profit_recovery:,.2f} Profit Recovery" if profit_recovery > 0 else "₹0.00"
        )

    with col_sim2:
        st.success(
            f"🎯 **Scenario Result**: By enforcing a strict **{max_discount_cap*100:.0f}% discount cap**, "
            f"the company recovers **₹{profit_recovery:,.2f}** in net profit, boosting total profit margin "
            f"from **{(orig_total_profit/df['Sales'].sum())*100:.1f}%** to **{(sim_total_profit/sim_df['New Sales'].sum())*100:.1f}%**!"
        )
