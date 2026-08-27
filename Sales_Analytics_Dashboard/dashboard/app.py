import sys
import os
import streamlit as st
import pandas as pd
import numpy as np

# Add project root and parent directories to sys.path for Streamlit Cloud compatibility
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PARENT_DIR = os.path.abspath(os.path.join(ROOT_DIR, ".."))

for path_entry in [ROOT_DIR, PARENT_DIR, CURRENT_DIR]:
    if path_entry not in sys.path:
        sys.path.insert(0, path_entry)

try:
    from src.data_cleaning import load_raw_data, clean_sales_data, save_processed_data
    from src.feature_engineering import apply_feature_engineering
    from dashboard.components.overview import render_overview_page
    from dashboard.components.sales_analysis import render_sales_analysis_page
    from dashboard.components.profitability import render_profitability_page
    from dashboard.components.product_analysis import render_product_analysis_page
    from dashboard.components.forecasting_page import render_forecasting_page
except ModuleNotFoundError:
    from Sales_Analytics_Dashboard.src.data_cleaning import load_raw_data, clean_sales_data, save_processed_data
    from Sales_Analytics_Dashboard.src.feature_engineering import apply_feature_engineering
    from Sales_Analytics_Dashboard.dashboard.components.overview import render_overview_page
    from Sales_Analytics_Dashboard.dashboard.components.sales_analysis import render_sales_analysis_page
    from Sales_Analytics_Dashboard.dashboard.components.profitability import render_profitability_page
    from Sales_Analytics_Dashboard.dashboard.components.product_analysis import render_product_analysis_page
    from Sales_Analytics_Dashboard.dashboard.components.forecasting_page import render_forecasting_page

# Page Configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Theme-Adaptive CSS (Fully Compatible with System, Light & Dark Mode Toggles)
CUSTOM_CSS = """
<style>
    /* Streamlit Main Top Header Container */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 99999 !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Block Padding */
    .main .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.0rem !important;
    }

    /* Top Navigation Tabs - Adaptive Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background-color: var(--secondary-background-color, #1E293B) !important;
        padding: 6px 10px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        margin-bottom: 1.5rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px !important;
        white-space: nowrap !important;
        background-color: var(--background-color, #0F172A) !important;
        border-radius: 8px !important;
        color: var(--text-color, #F8FAFC) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0 18px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        border-color: #38BDF8 !important;
        color: #38BDF8 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-color: #3B82F6 !important;
    }

    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {
        color: #FFFFFF !important;
    }

    /* Sidebar Background & Borders */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color, #1E293B) !important;
        border-right: 1px solid rgba(128, 128, 128, 0.2) !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #38BDF8 !important;
        font-weight: 700 !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.4rem !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: var(--text-color) !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Adaptive Input Controls (Date Input, Multiselect, Selectbox) */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div {
        background-color: var(--background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    [data-testid="stDateInput"] input {
        color: var(--text-color) !important;
        -webkit-text-fill-color: var(--text-color) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* BaseWeb Calendar & Dropdown Popovers */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="calendar"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-baseweb="popover"] *,
    div[data-baseweb="calendar"] *,
    div[data-baseweb="calendar"] button,
    div[data-baseweb="calendar"] div,
    div[data-baseweb="calendar"] span,
    div[data-baseweb="menu"] * {
        color: var(--text-color) !important;
        -webkit-text-fill-color: var(--text-color) !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="calendar"] [aria-selected="true"] {
        background-color: #3B82F6 !important;
    }

    div[data-baseweb="calendar"] [aria-selected="true"] *,
    div[data-baseweb="calendar"] [aria-selected="true"] div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Multiselect Tags */
    [data-baseweb="tag"] {
        background-color: #3B82F6 !important;
        border-radius: 6px !important;
    }

    [data-baseweb="tag"] span,
    [data-baseweb="tag"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Executive Metric Cards */
    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 14px 16px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    [data-testid="stMetricLabel"] p {
        color: var(--text-color) !important;
        opacity: 0.8 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] div {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }

    /* Header Gradient Title */
    .main-title {
        background: linear-gradient(90deg, #38BDF8, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: var(--text-color);
        opacity: 0.8;
        font-size: 1.0rem;
        margin-bottom: 1.2rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_data
def load_dataset() -> pd.DataFrame:
    """
    Loads processed dataset with caching. Runs pipeline if processed data missing.
    """
    processed_path = os.path.join(ROOT_DIR, "data", "processed", "sales_data_cleaned.csv")
    raw_path = os.path.join(ROOT_DIR, "data", "raw", "sample_superstore.csv")

    if not os.path.exists(processed_path):
        if not os.path.exists(raw_path):
            st.error("Raw data file missing. Please ensure sample_superstore.csv is in data/raw/")
            st.stop()
        raw_df = load_raw_data(raw_path)
        cleaned_df = clean_sales_data(raw_df)
        df = apply_feature_engineering(cleaned_df)
        save_processed_data(df, processed_path)
    else:
        df = pd.read_csv(processed_path)
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        if 'Ship Date' in df.columns:
            df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
            
    return df

def main():
    df = load_dataset()

    # App Header
    st.markdown('<div class="main-title">Sales Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Executive Business Intelligence • Revenue & Profit Performance • Predictive Forecasting</div>', unsafe_allow_html=True)

    # Sidebar Header & Global Filters
    st.sidebar.markdown("## 📈 Sales BI Platform")
    st.sidebar.markdown("### 🔍 Global Filters")

    # Date Range Filter
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Multi-Select Filters
    all_years = sorted(df['Year'].dropna().unique().astype(int).tolist())
    selected_years = st.sidebar.multiselect("Select Years", options=all_years, default=all_years)

    all_regions = sorted(df['Region'].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect("Select Regions", options=all_regions, default=all_regions)

    all_categories = sorted(df['Category'].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect("Select Categories", options=all_categories, default=all_categories)

    all_segments = sorted(df['Segment'].dropna().unique().tolist())
    selected_segments = st.sidebar.multiselect("Select Customer Segments", options=all_segments, default=all_segments)

    # Apply Filters to DataFrame
    filtered_df = df.copy()

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
        filtered_df = filtered_df[
            (filtered_df['Order Date'].dt.date >= start_d) & 
            (filtered_df['Order Date'].dt.date <= end_d)
        ]

    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]

    if selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

    if selected_segments:
        filtered_df = filtered_df[filtered_df['Segment'].isin(selected_segments)]

    # Validate non-empty data
    if filtered_df.empty:
        st.warning("⚠️ No data available matching the selected filter criteria. Please broaden your selection.")
        st.stop()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Showing {len(filtered_df):,} out of {len(df):,} total orders.**")

    # Main Top Navigation Bar (Always Visible at top of page)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Overview",
        "🗺️ Sales & Regional Analysis",
        "💸 Profitability Analysis",
        "📦 Product & Customer Intelligence",
        "🔮 Predictive Forecasting"
    ])

    with tab1:
        render_overview_page(filtered_df)

    with tab2:
        render_sales_analysis_page(filtered_df)

    with tab3:
        render_profitability_page(filtered_df)

    with tab4:
        render_product_analysis_page(filtered_df)

    with tab5:
        render_forecasting_page(filtered_df)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
        "Sales Analytics Dashboard • Built with Python, Pandas, Plotly & Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
