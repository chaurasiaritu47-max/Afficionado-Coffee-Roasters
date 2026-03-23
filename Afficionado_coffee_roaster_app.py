import streamlit as st
st.set_page_config(page_title="Afficionado Coffee Roasters Dashboard", page_icon="☕", layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
     
st.markdown("""
<style>

.stApp {
    background-color: #F5F0E7;     /* light beige background */
}

[data-testid="stSidebar"] *{
    background-color: #4b2e2b;    /* coffee brown sidebar */
    color: white;
}

h1 {
    text-align: center;   
    color: #3e2723;     \* dark brown title color */
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #1a237e !important;   \* indigo kpi values */
}

[data-testid="stMetricLabel"] {
    color: #4e342e !important;            /* dark brown kpi labels */
    
}

div[data-testid="stMetric"] {
    background-color: #f0f8ff;
    border: 2px solid #4B2E2B;   /* kpi border */
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    
}
h2 {
    color: #4e342e;     \* dark brown chart title color */
    font-weight: 600;
}


</style>
""", unsafe_allow_html=True)

st.title(" ☕ Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters") 
df = pd.read_csv("final_Afficionado_Coffee_Roasters.csv")

filtered_df = df.copy()
# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

# Category filter
category_filter = st.sidebar.multiselect("Select Category",options=filtered_df["product_category"].unique())
if category_filter:
    temp_df = filtered_df[filtered_df["product_category"].isin(category_filter)]
else:
    temp_df = filtered_df

# Product type filter
type_filter = st.sidebar.multiselect("Select Product Type",options=temp_df["product_type"].unique())
# Store location filter

location_filter = st.sidebar.multiselect("Select Store Location",options=temp_df["store_location"].unique())

# Top number products
top_n = st.sidebar.slider("Select Top N Products",min_value=5,max_value=20,value=10)

if category_filter:
    filtered_df = filtered_df[filtered_df["product_category"].isin(category_filter)]

if type_filter:
    filtered_df = filtered_df[filtered_df["product_type"].isin(type_filter)]

if location_filter:
    filtered_df = filtered_df[filtered_df["store_location"].isin(location_filter)]


# Total Revenue
total_revenue = filtered_df["Revenue"].sum()

# Product Sales Volume
total_units_sold = filtered_df["transaction_qty"].sum()

# Category Revenue Share (highest category share)
# If select only one category, that becomes 100% of the filtered revenue, so it shows 100%. 
#When select multiple categories, the revenue gets divided between them, so the percentage changes.
category_revenue = filtered_df.groupby("product_category")["Revenue"].sum().sort_values(ascending=False)
if total_revenue > 0 and len(category_revenue) > 0:
    top_category_revenue = category_revenue.iloc[0]
    top_category_share = (top_category_revenue / total_revenue) * 100
else:
    top_category_share = 0

# Revenue Concentration Ratio 
#When only one product type is selected, the no.ofproducts becomes very small and the top 20% calculation become 0 products
#so it shows 0%. When multiple product types are selected, more products exist and the ratio shows a value.
product_revenue = filtered_df.groupby("product_id")["Revenue"].sum().sort_values(ascending=False)
top_20_products = int(len(product_revenue) * 0.2)
top_revenue = product_revenue.head(top_20_products).sum()
revenue_concentration_ratio = (top_revenue / total_revenue) * 100

# Product Revenue Contribution
product_revenue_share = (product_revenue / total_revenue) * 100
top_product_share = product_revenue_share.max()


# Product Efficiency Score 
product_efficiency = product_revenue.mean()


# AUTOMATIC INSIGHT SUMMARY
top_product = filtered_df.groupby("product_detail")["Revenue"].sum().idxmax()
top_category = filtered_df.groupby("product_category")["Revenue"].sum().idxmax()
top_store = filtered_df.groupby("store_location")["Revenue"].sum().idxmax()

st.markdown(
f"""
<div style="background-color:#90EE90; padding:15px; border-radius:10px;">

📊 <b>Dashboard Insights</b>

• The <b>top revenue generating product</b> is <b>{top_product}</b>.  
• The <b>highest revenue category</b> is <b>{top_category}</b>.  
• The <b>best performing store location</b> is <b>{top_store}</b>.  

</div>
""",
unsafe_allow_html=True
)


st.markdown("### 📌 Key Business Metrics")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Total Revenue", f"${total_revenue:,.0f}")
with col2:
    st.metric("Product Sales Volume", f"{total_units_sold:,}")
with col3:
    st.metric("Category Revenue Share", f"{top_category_share:.2f}%")
with col4:
    st.metric("Revenue Concentration Ratio", f"{revenue_concentration_ratio:.2f}%")
with col5:
    st.metric("Product Revenue Contribution", f"{top_product_share:.2f}%")
with col6:
    st.metric("Product Efficiency Score", f"${product_efficiency:,.2f}")

st.divider()




st.markdown("### 📊 Product Sales Analysis")
st.divider()
col1, space, col2 = st.columns([1,0.2,1])
# prodct ranking by volume
with col1:
    st.subheader("Products by Sales Volume")
    fig, ax = plt.subplots()
    filtered_df.groupby("product_detail")["transaction_qty"].sum().sort_values(ascending=False).head(top_n).plot(kind='bar', ax=ax, color='#D77A3F')
    ax.set_xlabel("Products", color='#2B2222', fontsize=12)
    ax.set_ylabel("Sales Volume", color='#2B2222', fontsize=12)
    ax.tick_params(axis='x', colors='#1a237e', labelsize=11)
    ax.tick_params(axis='y', colors='#1a237e', labelsize=11)
    fig.patch.set_facecolor('#F5F0E7')     # used to color the chart background
    ax.set_facecolor('#f0f8ff')             # used to color the area inside the chart
    st.pyplot(fig)

#product ranking by revenue
with col2:
    st.subheader("Products by Revenue")
    fig, ax = plt.subplots()
    filtered_df.groupby("product_detail")["Revenue"].sum().sort_values(ascending=False).head(top_n).plot(kind='bar', ax=ax, color='#D77A3F')
    ax.set_xlabel("Products", color='#2B2222', fontsize=12)
    ax.set_ylabel("Revenue", color='#2B2222', fontsize=12)
    ax.tick_params(axis='x', colors='darkblue', labelsize=11)
    ax.tick_params(axis='y', colors='darkblue', labelsize=11)
    fig.patch.set_facecolor('#F5F0E7')   
    ax.set_facecolor('#f0f8ff')
    st.pyplot(fig)
st.divider()
st.markdown("### 📈 Revenue Distribution Analysis")
st.divider()
col3, space, col4 = st.columns([1,0.2,1])
# category revenue distribution
with col3:
    st.subheader("Revenue by Category")
    fig, ax = plt.subplots()
    filtered_df.groupby("product_category")["Revenue"].sum().plot(kind='bar', ax=ax, color='#D77A3F')
    ax.set_xlabel("Category", color='#2B2222', fontsize=12)
    ax.set_ylabel("Revenue", color='#2B2222', fontsize=12)
    ax.tick_params(axis='x', colors='darkblue', labelsize=11)
    ax.tick_params(axis='y', colors='darkblue', labelsize=11)
    fig.patch.set_facecolor('#F5F0E7')   
    ax.set_facecolor('#f0f8ff')
    st.pyplot(fig)
    

# product performance table
with col4:
    st.subheader("Revenue by Store Location")
    fig, ax = plt.subplots()
    filtered_df.groupby("store_location")["Revenue"].sum().sort_values(ascending=False).plot(kind='bar', ax=ax, color='#D77A3F')
    ax.set_xlabel("Store Location", color='#2B2222', fontsize=12)
    ax.set_ylabel("Revenue", color='#2B2222', fontsize=12)
    ax.tick_params(axis='x', colors='#1a237e', labelsize=11)
    ax.tick_params(axis='y', colors='#1a237e', labelsize=11)
    fig.patch.set_facecolor('#F5F0E7')   
    ax.set_facecolor('#f0f8ff')
    st.pyplot(fig)
   
st.divider()
st.markdown("### 🔎 Product Performance Insights")
st.divider()
col5, space, col6 = st.columns([1,0.2,1])
#product popularity vs revenue
with col5:
    st.subheader("Sale Volume vs Revenue")
    fig, ax = plt.subplots()
    product_analysis = filtered_df.groupby("product_detail").agg({"transaction_qty":"sum","Revenue":"sum"})
    scatter = ax.scatter(product_analysis["transaction_qty"],product_analysis["Revenue"],color="#D77A3F",alpha=0.7)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xlabel("Sales Volume", color='#2B2222', fontsize=12)
    ax.set_ylabel("Revenue", color='#2B2222', fontsize=12)
    ax.tick_params(axis='x', colors='#1a237e', labelsize=11)
    ax.tick_params(axis='y', colors='#1a237e', labelsize=11)
    fig.patch.set_facecolor('#F5F0E7')  # for coloring the chart background
    ax.set_facecolor('#f0f8ff')          # for coloring the area inside the chart
    st.pyplot(fig)

# sales by store location
with col6:
    st.subheader("Product Performance Table")
    product_table = filtered_df.groupby("product_detail").agg({"transaction_qty":"sum","Revenue":"sum"}).sort_values("Revenue", ascending=False)
# Apply color styling
    styled_table = product_table.style.format({"transaction_qty":"{:,}", "Revenue":"${:,.2f}"}).set_properties(**{'color':'#1a237e'})
    st.dataframe(styled_table)
