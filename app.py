# =========================================================
# IMPORT LIBRARIES
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="WinPower Sales Dashboard",
    page_icon="🔋",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🔋 WinPower Sales EDA Dashboard")
st.markdown("Comprehensive Sales Analytics Dashboard")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/eda_dataset_winpower.csv")

    date_cols = ['Billing_date', 'Delivery_date', 'Due_date']

    for col in date_cols:
        df[col] = pd.to_datetime(df[col])

    return df

df = load_data()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Dashboard Overview",
        "Sales Analysis",
        "Product Analysis",
        "Zone Analysis",
        "Regional Manager",
        "Customer Analysis",
        "Payment Analysis",
        "Return Analysis",
        "Time Series Analysis",
        "Correlation Analysis",
        "Raw Dataset"
    ]
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = df['Sales_amount'].sum()
total_vat = df['VAT_amount'].sum()
total_discount = df['Discount_amount'].sum()
total_quantity = df['Quantity'].sum()

# =========================================================
# DASHBOARD OVERVIEW
# =========================================================

if page == "Dashboard Overview":

    st.header("📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"{total_sales:,.2f}")
    col2.metric("Total VAT", f"{total_vat:,.2f}")
    col3.metric("Total Discount", f"{total_discount:,.2f}")
    col4.metric("Total Quantity", f"{total_quantity:,.0f}")

    st.divider()

    st.subheader("Monthly Sales Trend")

    monthly_sales = df.groupby(
        df['Billing_date'].dt.month
    )['Sales_amount'].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(monthly_sales.index, monthly_sales.values, marker='o')

    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.set_title("Monthly Sales Trend")

    st.pyplot(fig)

# =========================================================
# SALES ANALYSIS
# =========================================================

elif page == "Sales Analysis":

    st.header("💰 Sales Analysis")

    sales_zone = df.groupby('Sales_zone')['Sales_amount'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12,6))

    sales_zone.plot(kind='bar', ax=ax)

    ax.set_title("Sales by Zone")
    ax.set_ylabel("Sales Amount")

    st.pyplot(fig)

    st.divider()

    st.subheader("Sales Distribution")

    fig, ax = plt.subplots(figsize=(10,5))

    sns.histplot(df['Sales_amount'], kde=True, ax=ax)

    st.pyplot(fig)

# =========================================================
# PRODUCT ANALYSIS
# =========================================================

elif page == "Product Analysis":

    st.header("🔋 Product Analysis")

    top_products = df.groupby(
        'Product_name'
    )['Sales_amount'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12,6))

    top_products.plot(kind='bar', ax=ax)

    ax.set_title("Top 10 Products")
    ax.set_ylabel("Sales Amount")

    st.pyplot(fig)

    st.divider()

    st.subheader("Battery Type Distribution")

    battery_type = df.groupby(
        'Battery_type'
    )['Sales_amount'].sum()

    fig2, ax2 = plt.subplots(figsize=(8,8))

    battery_type.plot(
        kind='pie',
        autopct='%1.1f%%',
        ax=ax2
    )

    ax2.set_ylabel("")

    st.pyplot(fig2)

# =========================================================
# ZONE ANALYSIS
# =========================================================

elif page == "Zone Analysis":

    st.header("🌍 Zone Analysis")

    zone_sales = df.groupby(
        'Sales_zone'
    )['Sales_amount'].sum().sort_values(ascending=False)

    zone_discount = df.groupby(
        'Sales_zone'
    )['Discount_amount'].sum()

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(8,5))

        zone_sales.plot(kind='bar', ax=ax)

        ax.set_title("Zone Wise Sales")

        st.pyplot(fig)

    with col2:

        fig2, ax2 = plt.subplots(figsize=(8,5))

        zone_discount.plot(kind='bar', ax=ax2)

        ax2.set_title("Zone Wise Discount")

        st.pyplot(fig2)

# =========================================================
# REGIONAL MANAGER ANALYSIS
# =========================================================

elif page == "Regional Manager":

    st.header("👨‍💼 Regional Manager Analysis")

    manager_sales = df.groupby(
        'Region_manager'
    )['Sales_amount'].sum().sort_values(ascending=False)

    manager_vat = df.groupby(
        'Region_manager'
    )['VAT_amount'].sum()

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(8,5))

        manager_sales.plot(kind='bar', ax=ax)

        ax.set_title("Manager Wise Sales")

        st.pyplot(fig)

    with col2:

        fig2, ax2 = plt.subplots(figsize=(8,5))

        manager_vat.plot(kind='bar', ax=ax2)

        ax2.set_title("Manager Wise VAT")

        st.pyplot(fig2)

# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

elif page == "Customer Analysis":

    st.header("👥 Customer Analysis")

    customer_sales = df.groupby(
        'Customer_type'
    )['Sales_amount'].sum()

    fig, ax = plt.subplots(figsize=(8,5))

    customer_sales.plot(kind='bar', ax=ax)

    ax.set_title("Customer Type Sales")

    st.pyplot(fig)

    st.divider()

    top_customers = df.groupby(
        'Customer_name'
    )['Sales_amount'].sum().sort_values(ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(12,5))

    top_customers.plot(kind='bar', ax=ax2)

    ax2.set_title("Top 10 Customers")

    st.pyplot(fig2)

# =========================================================
# PAYMENT ANALYSIS
# =========================================================

elif page == "Payment Analysis":

    st.header("💳 Payment Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(6,5))

        sns.countplot(
            x='Payment_status',
            data=df,
            ax=ax
        )

        ax.set_title("Payment Status")

        st.pyplot(fig)

    with col2:

        fig2, ax2 = plt.subplots(figsize=(6,5))

        sns.countplot(
            x='Payment_method',
            data=df,
            ax=ax2
        )

        ax2.set_title("Payment Method")

        st.pyplot(fig2)

# =========================================================
# RETURN ANALYSIS
# =========================================================

elif page == "Return Analysis":

    st.header("↩️ Return Analysis")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.countplot(
        x='Return_status',
        data=df,
        ax=ax
    )

    ax.set_title("Return Status")

    st.pyplot(fig)

# =========================================================
# TIME SERIES ANALYSIS
# =========================================================

elif page == "Time Series Analysis":

    st.header("📈 Time Series Analysis")

    monthly_sales = df.groupby(
        df['Billing_date'].dt.month
    )['Sales_amount'].sum()

    daily_sales = df.groupby(
        df['Billing_date'].dt.day
    )['Sales_amount'].sum()

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(8,5))

        ax.plot(
            monthly_sales.index,
            monthly_sales.values,
            marker='o'
        )

        ax.set_title("Monthly Sales Trend")

        st.pyplot(fig)

    with col2:

        fig2, ax2 = plt.subplots(figsize=(8,5))

        ax2.plot(
            daily_sales.index,
            daily_sales.values
        )

        ax2.set_title("Daily Sales Trend")

        st.pyplot(fig2)

# =========================================================
# CORRELATION ANALYSIS
# =========================================================

elif page == "Correlation Analysis":

    st.header("🔥 Correlation Heatmap")

    numeric_cols = [
        'Quantity',
        'Unit_price_pcs',
        'Amount',
        'Discount_percent',
        'Discount_amount',
        'VAT_amount',
        'Sales_amount'
    ]

    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10,7))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        ax=ax
    )

    st.pyplot(fig)

# =========================================================
# RAW DATASET
# =========================================================

elif page == "Raw Dataset":

    st.header("🗂️ Raw Dataset")

    st.dataframe(df)

    st.write("Dataset Shape:", df.shape)

# =========================================================
# FOOTER
# =========================================================

st.sidebar.markdown("---")
st.sidebar.info("Mujakkir Ahmad | Data Analyst | [GitHub](https://github.com/mujakkirdv)")