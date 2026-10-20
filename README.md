<<<<<<< HEAD
# Retail Sales & Profitability Analysis (EDA)

A comprehensive, hypothesis-driven Exploratory Data Analysis (EDA) and interactive business intelligence dashboard diagnosing pricing efficiency, seasonal trends, and profit margin leakages using statistical testing and multi-panel visualizations.

---

## 📌 Project Overview
- **Domain**: Retail E-Commerce Analytics & Profitability Optimization
- **Key Business Diagnostics**:
  1. Distribution and skewness of revenue, quantity, and profit across product lines.
  2. Empirical relationship between promotional discounts and net profitability (Testing the "Discount Cliff").
  3. Significance testing of customer segment profitability (Consumer, Corporate, Home Office).
  4. Identification of loss-making product categories and sub-categories.
  5. Regional performance disparities and shipping efficiency.
  6. Seasonality and holiday cycles across fiscal quarters.

---

## 🔬 Statistical Hypothesis Tests
- **Pearson Correlation Test**: Evaluates the linear relationship between `discount` and `profit` ($r = -0.528, p < 10^{-179}$), proving steep discounts directly erode operating margin.
- **One-Way ANOVA (Analysis of Variance)**: Evaluates whether mean profitability varies significantly across Customer Segments ($F = 0.415, p = 0.660$).
- **Welch's Two-Sample Independent t-Test**: Proves `Technology` delivers statistically significantly higher net profit margins than `Furniture` ($t = 11.95, p < 10^{-30}$).
- **IQR (Interquartile Range) Outlier Detection**: Identifies severe loss-making outlier transactions and extreme high-value orders.

---

## 📂 Repository Structure
```text
├── data/
│   └── superstore_sales.csv                 # Retail transactions dataset (2,500 orders)
├── visualizations/
│   ├── 01_sales_profit_distributions.png    # Histograms & Boxplots
│   ├── 02_correlation_matrix_heatmap.png    # Correlation heatmap
│   ├── 03_category_profitability_breakdown.png # Category & Subcategory profit
│   ├── 04_discount_vs_profit_loss_curve.png # Discount margin impact curve
│   ├── 05_monthly_sales_seasonality_trend.png # Monthly revenue & profit trend
│   └── 06_regional_profit_performance.png   # Regional segment performance
├── reports/
│   └── eda_executive_summary.md             # Executive recommendations
├── data_generator.py                        # Dataset creation pipeline
├── eda_analysis.py                          # Full EDA pipeline & tests
├── eda_dashboard.py                         # Interactive Streamlit dashboard
├── requirements.txt                         # Dependencies
└── README.md                                # Project documentation
```

---

## 🚀 Running the Project

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run the Statistical EDA Pipeline
```bash
python eda_analysis.py
```
This generates:
- Statistical console logs & hypothesis test outcomes
- 6 publication-ready charts in `visualizations/`
- Markdown strategic summary in `reports/eda_executive_summary.md`

### 3. Launch the Interactive Dashboard
```bash
streamlit run eda_dashboard.py
```
Features:
- **Custom CSV Uploader**: Upload any sales dataset or use the built-in generator.
- **Dynamic KPI Cards**: Real-time sales, net profit, margin %, deficit orders, and avg discount.
- **The "Discount Cliff" Simulator**: Test discount caps and observe simulated profit recovery in real-time.
- **Live Hypothesis Testing Engine**: Dynamic Pearson correlation, ANOVA, and Welch's t-test.
- **Outlier Explorer**: Interquartile range outlier detection with CSV data export.

---

## 📈 Strategic Business Takeaways
1. **Discount Cap Policy**: Capping discounts at 20% eliminates the vast majority of negative-margin transactions.
2. **Prioritize Technology Line**: Technology delivers the highest operating profit margin and stable unit economics.
3. **Q4 Demand Preparation**: Strong cyclical spikes in November and December require proactive inventory allocation.
=======
# code-alpha-EDA
>>>>>>> 631ea12023591962a37025932ffbdbe9146183e8
