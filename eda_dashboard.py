"""
Retail Sales & Profitability Analysis Dashboard
Interactive Executive Analytics, Outlier Diagnostics & Dynamic Pricing Simulator
"""

import os
import sys
import random
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(
    page_title="Retail Sales & Profitability Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 50%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.02rem;
        color: #94a3b8;
        margin-bottom: 1.2rem;
    }
    /* Modern Dashboard Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        padding: 4px 0px 10px 0px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre-wrap;
        background-color: rgba(148, 163, 184, 0.1) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        font-weight: 600;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] span {
        color: var(--text-color, #cbd5e1) !important;
        font-size: 0.94rem;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(148, 163, 184, 0.22) !important;
        border-color: rgba(148, 163, 184, 0.45) !important;
    }
    .stTabs [data-baseweb="tab"]:hover p,
    .stTabs [data-baseweb="tab"]:hover div,
    .stTabs [data-baseweb="tab"]:hover span {
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        border: 1px solid #60a5fa !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] div,
    .stTabs [aria-selected="true"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


def generate_retail_dataset(num_records=2500, seed=42):
    """Generate realistic Superstore retail dataset dynamically with zero external dependencies."""
    np.random.seed(seed)
    random.seed(seed)

    categories_subcategories = {
        "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Binders", "Storage", "Paper", "Art", "Appliances", "Envelopes", "Labels"]
    }
    segments = ["Consumer", "Corporate", "Home Office"]
    segment_weights = [0.52, 0.30, 0.18]
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_mode_weights = [0.60, 0.20, 0.15, 0.05]
    regions_states = {
        "West": ["California", "Washington", "Oregon", "Nevada", "Arizona", "Colorado"],
        "East": ["New York", "Pennsylvania", "Massachusetts", "New Jersey", "Ohio"],
        "Central": ["Illinois", "Texas", "Michigan", "Indiana", "Wisconsin", "Minnesota"],
        "South": ["Florida", "North Carolina", "Virginia", "Georgia", "Tennessee"]
    }

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days
    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-2024-{100000 + i}"
        customer_id = f"CUST-{random.randint(1001, 1450):04d}"
        customer_name = f"Client {customer_id.split('-')[1]}"
        segment = np.random.choice(segments, p=segment_weights)

        region = random.choice(list(regions_states.keys()))
        state = random.choice(regions_states[region])
        city = f"{state} City"
        postal_code = random.randint(10001, 99950)

        day_offset = random.randint(0, days_range)
        order_date = start_date + timedelta(days=day_offset)
        if order_date.month in [11, 12] and random.random() < 0.35:
            day_offset = random.randint(0, days_range)

        ship_mode = np.random.choice(ship_modes, p=ship_mode_weights)
        ship_days = 0 if ship_mode == "Same Day" else (random.randint(1, 3) if ship_mode == "First Class" else random.randint(4, 7))
        ship_date = order_date + timedelta(days=ship_days)

        category = random.choice(list(categories_subcategories.keys()))
        sub_category = random.choice(categories_subcategories[category])
        product_id = f"{category[:3].upper()}-{sub_category[:3].upper()}-{random.randint(100, 999)}"
        product_name = f"{sub_category} Model {random.randint(10, 99)} Pro"

        quantity = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01])

        if category == "Technology":
            base_price = np.random.gamma(shape=3.5, scale=120) + 40
            target_margin = np.random.normal(0.28, 0.06)
            discount_prob = 0.30
        elif category == "Furniture":
            base_price = np.random.gamma(shape=2.5, scale=90) + 25
            target_margin = np.random.normal(0.06, 0.08)
            discount_prob = 0.55
        else:
            base_price = np.random.gamma(shape=1.8, scale=25) + 3
            target_margin = np.random.normal(0.24, 0.05)
            discount_prob = 0.40

        unit_price = round(max(1.99, base_price), 2)
        total_list_sales = unit_price * quantity
        discount = np.random.choice([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8], p=[0.25, 0.20, 0.20, 0.15, 0.08, 0.06, 0.04, 0.02]) if random.random() < discount_prob else 0.0

        sales = round(total_list_sales * (1.0 - discount), 2)
        cogs = round(total_list_sales * (1.0 - target_margin), 2)
        profit = round(sales - cogs, 2)
        profit_margin_pct = round((profit / sales) * 100, 2) if sales > 0 else 0.0

        records.append({
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "ship_mode": ship_mode,
            "shipping_days": ship_days,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "segment": segment,
            "country": "United States",
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "region": region,
            "product_id": product_id,
            "category": category,
            "sub_category": sub_category,
            "product_name": product_name,
            "sales": sales,
            "quantity": quantity,
            "discount": discount,
            "profit": profit,
            "profit_margin_pct": profit_margin_pct
        })

    return pd.DataFrame(records)


# ==========================================
# SIDEBAR: DATA INPUT SELECTION
# ==========================================
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Retail Analytics System")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Data Source")

data_source = st.sidebar.radio(
    "Select Data Source:",
    [
        "📁 Upload My Own Dataset (CSV / Excel)",
        "📊 System Default Dataset (2,500 Orders)",
        "⚡ Generate Custom Dataset"
    ]
)

df_loaded = None

if data_source == "📁 Upload My Own Dataset (CSV / Excel)":
    uploaded_file = st.sidebar.file_uploader("Upload your sales CSV / Excel file:", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_loaded = pd.read_csv(uploaded_file)
            else:
                df_loaded = pd.read_excel(uploaded_file)
            st.sidebar.success(f"Loaded {len(df_loaded):,} rows from file!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
    else:
        st.sidebar.info("Upload a dataset to evaluate your retail data, or switch to System Default.")

elif data_source == "⚡ Generate Custom Dataset":
    num_gen = st.sidebar.slider("Number of Orders:", min_value=200, max_value=10000, value=2500, step=100)
    rand_seed = st.sidebar.number_input("Random Seed:", value=42, step=1)
    if st.sidebar.button("🎲 Generate Fresh Dataset", type="primary"):
        st.session_state["generated_eda_df"] = generate_retail_dataset(num_records=num_gen, seed=int(rand_seed))
        st.sidebar.success(f"Generated {num_gen:,} fresh records!")

    if "generated_eda_df" in st.session_state:
        df_loaded = st.session_state["generated_eda_df"]
    else:
        df_loaded = generate_retail_dataset(num_records=num_gen, seed=int(rand_seed))

else:
    # Default system dataset path
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "superstore_sales.csv"),
        os.path.join("CodeAlpha_EDA", "data", "superstore_sales.csv"),
        os.path.join("sample_data", "sample_superstore_eda.csv"),
        "superstore_sales.csv"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            df_loaded = pd.read_csv(p)
            break

    if df_loaded is None:
        df_loaded = generate_retail_dataset(num_records=2500, seed=42)

# Fallback guarantee
if df_loaded is None or df_loaded.empty:
    df_loaded = generate_retail_dataset(num_records=2500, seed=42)

# ==========================================
# INTELLIGENT COLUMN STANDARDIZATION
# ==========================================
col_map = {c.lower().strip(): c for c in df_loaded.columns}

def safe_col(names, fallback=None):
    for n in names:
        if n.lower() in col_map:
            return col_map[n.lower()]
    return fallback

sales_col = safe_col(["sales", "revenue", "amount", "total_sales"], fallback="sales")
profit_col = safe_col(["profit", "net_profit", "earnings", "margin"], fallback="profit")
discount_col = safe_col(["discount", "disc", "discount_rate"], fallback="discount")
category_col = safe_col(["category", "dept", "department"], fallback="category")
subcategory_col = safe_col(["sub_category", "subcategory", "sub-category", "item_group"], fallback="sub_category")
region_col = safe_col(["region", "zone", "territory", "area"], fallback="region")
segment_col = safe_col(["segment", "customer_segment", "client_type"], fallback="segment")
date_col = safe_col(["order_date", "date", "transaction_date", "invoice_date"], fallback="order_date")

df = df_loaded.copy()

df["sales"] = pd.to_numeric(df[sales_col], errors="coerce").fillna(0.0) if sales_col in df.columns else 100.0
df["profit"] = pd.to_numeric(df[profit_col], errors="coerce").fillna(0.0) if profit_col in df.columns else df["sales"] * 0.15
df["discount"] = pd.to_numeric(df[discount_col], errors="coerce").fillna(0.0) if discount_col in df.columns else 0.0
if df["discount"].max() > 1.0:
    df["discount"] = df["discount"] / 100.0

df["category"] = df[category_col].astype(str) if category_col in df.columns else "General"
df["sub_category"] = df[subcategory_col].astype(str) if subcategory_col in df.columns else df["category"]
df["region"] = df[region_col].astype(str) if region_col in df.columns else "General"
df["segment"] = df[segment_col].astype(str) if segment_col in df.columns else "General"

if date_col in df.columns:
    df["order_date"] = pd.to_datetime(df[date_col], errors="coerce").fillna(pd.Timestamp("2024-01-01"))
else:
    df["order_date"] = pd.date_range(start="2024-01-01", periods=len(df), freq="h")

df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
if "profit_margin_pct" not in df.columns:
    df["profit_margin_pct"] = np.where(df["sales"] > 0, (df["profit"] / df["sales"] * 100).round(2), 0.0)

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filter Dimensions")

min_d = df["order_date"].min().date()
max_d = df["order_date"].max().date()
date_range = st.sidebar.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

cat_options = sorted(df["category"].unique())
selected_cats = st.sidebar.multiselect("Category", cat_options, default=cat_options)

reg_options = sorted(df["region"].unique())
selected_regs = st.sidebar.multiselect("Region", reg_options, default=reg_options)

seg_options = sorted(df["segment"].unique())
selected_segs = st.sidebar.multiselect("Segment", seg_options, default=seg_options)

start_date_filter = date_range[0] if len(date_range) > 0 else min_d
end_date_filter = date_range[1] if len(date_range) > 1 else max_d

filtered_df = df[
    (df["order_date"].dt.date >= start_date_filter) &
    (df["order_date"].dt.date <= end_date_filter) &
    (df["category"].isin(selected_cats)) &
    (df["region"].isin(selected_regs)) &
    (df["segment"].isin(selected_segs))
]

if filtered_df.empty:
    st.warning("No records match your selected filter criteria. Showing full active dataset.")
    filtered_df = df.copy()

# Sidebar Download
st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Dataset Template")
csv_download = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="📥 Download CSV Dataset",
    data=csv_download,
    file_name="retail_sales_dataset.csv",
    mime="text/csv"
)

# ==========================================
# MAIN DASHBOARD INTERFACE
# ==========================================
st.markdown('<div class="main-title">📊 Retail Sales & Profitability Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hypothesis-Driven Exploratory Data Analysis, Outlier Diagnostics & Dynamic Pricing Simulator</div>', unsafe_allow_html=True)

# Top KPIs
tot_sales = filtered_df["sales"].sum()
tot_profit = filtered_df["profit"].sum()
net_margin = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0.0
tot_orders = len(filtered_df)
avg_disc = filtered_df["discount"].mean() * 100
loss_cnt = (filtered_df["profit"] < 0).sum()
loss_pct = (loss_cnt / tot_orders * 100) if tot_orders > 0 else 0.0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Revenue", f"${tot_sales:,.2f}", delta=f"{tot_orders:,} Orders")
k2.metric("📈 Net Profit", f"${tot_profit:,.2f}", delta=f"{net_margin:.2f}% Margin", delta_color="normal" if tot_profit >= 0 else "inverse")
k3.metric("🏷️ Avg Discount", f"{avg_disc:.1f}%")
k4.metric("🚨 Deficit Orders", f"{loss_cnt:,}", delta=f"-{loss_pct:.1f}% of volume", delta_color="inverse")
k5.metric("📦 Avg Order Value", f"${(tot_sales / tot_orders if tot_orders else 0):,.2f}")

st.markdown("---")

# Dashboard Tabs
tabs = st.tabs([
    "📈 Revenue & Seasonality",
    "📉 Discount Cliff & Profit Simulator",
    "🏢 Categories & Regions",
    "🔬 Statistical Hypothesis Engine",
    "📋 Outliers & Data Explorer"
])

# ----------------- TAB 1: Revenue & Seasonality -----------------
with tabs[0]:
    st.subheader("Monthly Sales & Profit Trajectory")
    monthly_trend = filtered_df.groupby("year_month").agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum")
    ).reset_index().sort_values("year_month")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=monthly_trend["year_month"], y=monthly_trend["total_sales"], name="Revenue ($)", marker_color="#2b5c8f", opacity=0.85))
    fig_trend.add_trace(go.Scatter(x=monthly_trend["year_month"], y=monthly_trend["total_profit"], name="Net Profit ($)", yaxis="y2", line=dict(color="#2ca02c", width=3), mode="lines+markers"))
    fig_trend.update_layout(
        title="Monthly Revenue vs Net Profit Over Time",
        yaxis=dict(title="Revenue ($)", showgrid=True),
        yaxis2=dict(title="Net Profit ($)", overlaying="y", side="right", showgrid=False),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.7)"),
        hovermode="x unified",
        height=450
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Revenue Share by Customer Segment")
        fig_seg = px.pie(filtered_df, names="segment", values="sales", hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_seg, use_container_width=True)

    with col_b:
        st.subheader("Regional Performance")
        reg_df = filtered_df.groupby("region").agg(sales=("sales", "sum"), profit=("profit", "sum")).reset_index()
        fig_reg = px.bar(reg_df, x="region", y=["sales", "profit"], barmode="group", color_discrete_map={"sales": "#1d3557", "profit": "#2a9d8f"})
        st.plotly_chart(fig_reg, use_container_width=True)

# ----------------- TAB 2: Discount Cliff & Profit Simulator -----------------
with tabs[1]:
    st.subheader("The 'Discount Cliff' Empirical Diagnostics")
    st.markdown("Examine how heavy price cuts erode operating profit and test dynamic discount ceilings:")

    col_sc, col_sim = st.columns([3, 2])
    with col_sc:
        fig_scatter = px.scatter(
            filtered_df,
            x="discount",
            y="profit",
            color="category",
            size="sales",
            hover_data=["sub_category"],
            title="Empirical Discount vs Net Profit (Bubble Size = Sales)",
            labels={"discount": "Promotional Discount (0.0 to 1.0)", "profit": "Net Profit ($)"},
            color_discrete_sequence=["#e63946", "#457b9d", "#2a9d8f"]
        )
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even ($0)")
        fig_scatter.update_layout(height=480)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_sim:
        st.markdown("### 🎚️ Interactive Discount Cap Simulator")
        st.caption("Simulate recovered margins if an executive discount ceiling is enforced.")
        sim_cap = st.slider("Enforce Maximum Allowable Discount (%)", min_value=10, max_value=80, value=20, step=5)
        sim_cap_dec = sim_cap / 100.0

        mask_over = filtered_df["discount"] > sim_cap_dec
        recovered = np.where(
            mask_over,
            filtered_df["sales"] * (filtered_df["discount"] - sim_cap_dec) / np.maximum(1 - filtered_df["discount"], 0.01),
            0.0
        )
        sim_total_profit = filtered_df["profit"].sum() + recovered.sum()
        profit_delta = sim_total_profit - tot_profit
        sim_loss_orders = ((filtered_df["profit"] + recovered) < 0).sum()

        st.metric("Simulated Net Profit", f"${sim_total_profit:,.2f}", delta=f"+${profit_delta:,.2f} Improvement")
        st.metric("Loss Orders with Cap", f"{sim_loss_orders:,}", delta=f"-{loss_cnt - sim_loss_orders:,} Cured Deficits", delta_color="inverse")
        st.info(f"""
        💡 **Executive Analysis**:
        A **{sim_cap}% Discount Cap** rescues **${profit_delta:,.2f}** in gross cash margins and converts 
        **{loss_cnt - sim_loss_orders}** loss-making transactions into profitable orders.
        """)

# ----------------- TAB 3: Categories & Regions -----------------
with tabs[2]:
    st.subheader("Category & Sub-Category Profitability Matrix")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cat_agg = filtered_df.groupby("category").agg(Sales=("sales", "sum"), Profit=("profit", "sum")).reset_index()
        fig_cat = px.bar(cat_agg, x="category", y=["Sales", "Profit"], barmode="group", title="Category Sales vs Profit Comparison")
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_c2:
        subcat_agg = filtered_df.groupby(["category", "sub_category"]).agg(Profit=("profit", "sum")).reset_index().sort_values("Profit", ascending=False)
        fig_subcat = px.bar(subcat_agg, x="Profit", y="sub_category", color="category", orientation="h", title="Sub-Category Net Margin Leaderboard")
        fig_subcat.add_vline(x=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_subcat, use_container_width=True)

# ----------------- TAB 4: Statistical Hypothesis Tests -----------------
with tabs[3]:
    st.subheader("Statistical Hypothesis Testing Engine")
    st.markdown("Live inferential tests recalculated in real time on active dataset:")

    col_h1, col_h2, col_h3 = st.columns(3)

    with col_h1:
        st.markdown("#### 1. Discount vs Profit (Pearson)")
        if len(filtered_df) > 2 and filtered_df["discount"].std() > 0:
            r_val, p_val = stats.pearsonr(filtered_df["discount"], filtered_df["profit"])
            st.metric("Pearson Correlation (r)", f"{r_val:.4f}")
            st.metric("p-value", f"{p_val:.3e}")
            if p_val < 0.05 and r_val < 0:
                st.success("✅ Statistically Significant Negative Impact (p < 0.05)")
            else:
                st.warning("⚠️ No statistically significant relationship")
        else:
            st.info("Insufficient variance in discount data.")

    with col_h2:
        st.markdown("#### 2. Segment Variance (ANOVA)")
        seg_groups = [g["profit"].values for _, g in filtered_df.groupby("segment") if len(g) > 1]
        if len(seg_groups) > 1:
            f_stat, p_anova = stats.f_oneway(*seg_groups)
            st.metric("ANOVA F-Statistic", f"{f_stat:.4f}")
            st.metric("p-value", f"{p_anova:.3e}")
            if p_anova < 0.05:
                st.success("✅ Significant profit variance across segments (p < 0.05)")
            else:
                st.info("ℹ️ Segments perform similarly")
        else:
            st.info("Single segment selected.")

    with col_h3:
        st.markdown("#### 3. Category Margin Comparison (t-Test)")
        cats_present = filtered_df["category"].unique()
        if len(cats_present) >= 2:
            c1_name = cats_present[0]
            c2_name = cats_present[1]
            c1_prof = filtered_df[filtered_df["category"] == c1_name]["profit"]
            c2_prof = filtered_df[filtered_df["category"] == c2_name]["profit"]
            if len(c1_prof) > 1 and len(c2_prof) > 1:
                t_stat, p_ttest = stats.ttest_ind(c1_prof, c2_prof, equal_var=False)
                st.metric(f"t-Stat ({c1_name[:8]} vs {c2_name[:8]})", f"{t_stat:.4f}")
                st.metric("p-value", f"{p_ttest:.3e}")
                if p_ttest < 0.05:
                    st.success("✅ Significant difference between categories (p < 0.05)")
                else:
                    st.info("ℹ️ Categories show comparable margins")
        else:
            st.info("Select at least 2 categories for comparison.")

# ----------------- TAB 5: Outliers & Data Explorer -----------------
with tabs[4]:
    st.subheader("IQR Outlier Detection & Interactive Data Browser")

    q1 = filtered_df["profit"].quantile(0.25)
    q3 = filtered_df["profit"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers_all = filtered_df[(filtered_df["profit"] < lower_bound) | (filtered_df["profit"] > upper_bound)]
    loss_outliers = filtered_df[filtered_df["profit"] < lower_bound]

    st.write(f"Detected **{len(outliers_all):,}** profit outliers ({len(outliers_all)/len(filtered_df)*100:.1f}% of active volume).")
    st.write(f"Severe Deficit Outliers (< ${lower_bound:.2f}): **{len(loss_outliers)}** high-risk transactions.")

    view_choice = st.radio("Display View:", ["Critical Deficit Outliers Only", "All Outliers (High & Low)", "Full Filtered Dataset"], horizontal=True)

    if view_choice == "Critical Deficit Outliers Only":
        display_tbl = loss_outliers
    elif view_choice == "All Outliers (High & Low)":
        display_tbl = outliers_all
    else:
        display_tbl = filtered_df

    st.dataframe(display_tbl, use_container_width=True, height=380)

    csv_data = display_tbl.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Displayed Table as CSV",
        data=csv_data,
        file_name="retail_sales_data.csv",
        mime="text/csv"
    )
