# 📈 Indian Sales Analytics Dashboard (₹ INR)

An end-to-end, interactive Business Intelligence & Sales Analytics platform built with **Python, Pandas, Plotly, Streamlit, and Statsmodels** using a real **Indian E-Commerce & Retail Sales Dataset**.

This platform analyzes retail sales performance, profitability, customer RFM segmentation, Indian state/city regional distribution, courier shipping modes, discount impact, and provides a **6-month Holt-Winters Exponential Smoothing predictive sales forecast** with interactive scenario modeling.

---

## 🎯 Project Objectives

1. **Executive Performance Monitoring**: Track top-line revenue (**₹64.73 Lakhs** / ₹6,472,530), net profit (**₹2.87 Lakhs** / ₹287,460), order volume (500), average order value (**₹12,945.06**), and overall profit margin (**4.44%**).
2. **Category & Sub-Category Intelligence**: Identify primary revenue drivers (**Electronics**: ₹24.79 Lakhs) and top profit generators (**Clothing**: ₹1.34 Lakhs).
3. **Discount Destruction Analysis**: Expose margin erosion caused by excessive discounts—discounts > 20% lead to a **28.4% order loss rate**.
4. **Geographical Performance Mapping**: Interactive Indian state ranking highlighting top revenue territories (**Central Region**: ₹21.67 Lakhs sales; **Maharashtra, Delhi, Karnataka, Tamil Nadu**).
5. **Customer RFM Segmentation**: Classify Indian customer base into Champions, Loyal Customers, At-Risk, and Lost tiers.
6. **Predictive Sales Forecasting & Scenario Modeling**: 6-month out-of-sample sales prediction with 95% confidence intervals and an interactive "What-If" discount restriction profit recovery simulator.

---

## 📁 Repository Structure

```
Sales_Analytics_Dashboard/
├── data/
│   ├── raw/
│   │   └── sample_superstore.csv        # Raw unaltered Indian sales dataset (1,500 rows)
│   └── processed/
│       └── sales_data_cleaned.csv     # Cleaned dataset with 34 derived features
├── notebooks/
│   └── sales_analysis.ipynb           # Complete Exploratory Data Analysis (EDA) notebook
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py               # Data loading, date parsing & integrity validation
│   ├── feature_engineering.py         # Time extraction, margin %, RFM & Pareto analysis
│   ├── analysis.py                    # KPI calculations & automated insight generators
│   ├── forecasting.py                 # Time-series aggregation & Holt-Winters model
│   └── visualization.py               # Dark theme Plotly chart components & styling (₹ INR)
├── dashboard/
│   ├── app.py                         # Streamlit multi-page application entrypoint
│   └── components/
│       ├── __init__.py
│       ├── overview.py                # Page 1: Executive Overview (India Market)
│       ├── sales_analysis.py          # Page 2: Regional Performance & Indian States
│       ├── profitability.py           # Page 3: Profitability & Discount Impact (₹)
│       ├── product_analysis.py        # Page 4: Product & Customer RFM Intelligence
│       └── forecasting_page.py        # Page 5: Predictive Forecasting & Scenario Simulator
├── tests/
│   └── test_pipeline.py               # Pytest automated test suite (100% pass rate)
├── requirements.txt                   # Dependency manifest
├── README.md                          # Comprehensive project documentation
└── .gitignore
```

---

## 📊 Dataset Information

* **Name**: Indian E-Commerce & Retail Sales Dataset
* **Geography**: India (Maharashtra, Delhi, Karnataka, Tamil Nadu, Uttar Pradesh, Gujarat, West Bengal, Madhya Pradesh, Rajasthan, Kerala, etc.)
* **Currency**: Indian Rupees (₹ INR)
* **Attributes (20 Raw Columns)**:
  * Order Identifiers: `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`
  * Customer Demographics: `Customer ID`, `Customer Name`, `Segment`
  * Geography: `Country` (India), `City`, `State`, `Postal Code` (PIN), `Region`
  * Product Hierarchy: `Product ID`, `Category`, `Sub-Category`, `Product Name`
  * Financials: `Sales` (₹), `Quantity`, `Discount`, `Profit` (₹)

---

## 🛠️ Technology Stack

* **Core Language**: Python 3.11
* **Data Processing & Analytics**: Pandas, NumPy
* **Data Visualization**: Plotly Express, Plotly Graph Objects
* **Web Dashboard**: Streamlit (Multi-page, custom dark glassmorphism styling)
* **Predictive Modeling**: Statsmodels (Holt-Winters Exponential Smoothing), Scikit-Learn
* **Testing & Quality Assurance**: Pytest, Nbformat

---

## 🔍 Key Findings & Business Insights (India Market)

1. **Revenue Leader**: **Electronics** is the #1 revenue engine in India (**₹24,79,005.00**).
2. **Profit Leader**: **Clothing** generates the highest total net profit (**₹1,33,956.00**).
3. **Loss-Making Category**: The **Tables** sub-category incurred a cumulative net loss of **₹-48,132.00**.
4. **Top Indian Territory**: The **Central** region (MP, CG) leads regional sales with **₹21,66,660.00** in sales and **₹1,03,524.00** in net profit.
5. **Discount Warning**: Orders discounted above **20%** suffer a **28.4% loss rate**, creating a net profit drain.

---

## 💡 Strategic Business Recommendations

1. **Cap Maximum Discounts at 15%**: Instantly recovers lost margin by halting high-discount profit destruction.
2. **Restructure Table Product Pricing**: Discontinue or re-price loss-leading Table models to eliminate the net drain.
3. **Expand High-Margin Clothing & Tech Inventory**: Re-allocate procurement budget towards top-performing Electronics and Clothing inventory.
4. **Implement VIP Customer Retention**: Establish dedicated account management for top RFM Champion customers across Tier-1 and Tier-2 Indian cities.

---

## 🚀 Installation & Running Instructions

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Clone & Setup Environment
```bash
cd "d:\3rd Sem\Yash Patil\Sales_Analytics_Dashboard"
```

### 3. Install Dependencies
```bash
py -3.11 -m pip install -r requirements.txt
```

### 4. Run Automated Unit Tests
```bash
py -3.11 -m pytest tests/test_pipeline.py
```

### 5. Launch Interactive Dashboard
```bash
py -3.11 -m streamlit run dashboard/app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.
