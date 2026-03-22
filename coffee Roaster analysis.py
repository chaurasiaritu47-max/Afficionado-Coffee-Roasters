import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv("D:\\python\\unified second project\\Afficionado_Coffee_Roasters.csv")

print(df.head(5))
print(df.info())
print(df.shape)
print(df.describe())
print("Null values:\n",df.isnull().sum())
duplicates=df.duplicated().sum()
print("Total duplicate row:",duplicates)
print("product id and unit price valid: \n",df[['product_id','unit_price']].head())
print("Unit Price Description:\n",df['unit_price'].describe())
print("Rows with zero or negative quantity:\n",df[df['transaction_qty'] <= 0])


# creating the revenue column as required
df['Revenue'] = df['transaction_qty'] * df['unit_price']
print(df.head(5))

df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S')
print(df.head(5))
print(df.info())

# top selling products
top_products = df.groupby('product_detail')['transaction_qty'].sum().sort_values(ascending=False)
print("top selling products:\n", top_products.head(10))

top_products.head(10).plot(kind='bar', figsize=(10,5))
plt.title("Top 10 Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# least selling products
least_products = df.groupby('product_detail')['transaction_qty'].sum().sort_values(ascending=True)
print("least selling products:\n", least_products.head(10))

least_products.head(10).plot(kind='bar', figsize=(10,5))
plt.title("Least Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# revenue by product detail
revenue_product = df.groupby('product_detail')['Revenue'].sum().sort_values(ascending=False)
print("Revenue by product:\n", revenue_product.head(10))

revenue_product.head(10).plot(kind='bar', figsize=(10,5))
plt.title("Top Revenue Generating Products")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# revenue by product category
category_revenue = df.groupby('product_category')['Revenue'].sum().sort_values(ascending=False)
print("Revenue by category:\n", category_revenue.head(10))
def autopct_format(pct):
    return ('%1.1f%%' % pct) if pct > 3 else ''   # hide very small percentages

plt.figure(figsize=(8,8))
category_revenue.plot(kind='pie',autopct=autopct_format,pctdistance=0.75,labels=None,startangle=90)
plt.title("Revenue Contribution by Product Category")
plt.legend(title="Product Category",labels=category_revenue.index,bbox_to_anchor=(1.25,1),loc="upper left")
plt.tight_layout()
plt.show()

# revanue by product type
revenue_type = df.groupby('product_type')['Revenue'].sum().sort_values(ascending=False)
print("Revenue by Product Type:\n", revenue_type)

revenue_type.plot(kind='bar', figsize=(8,5))
plt.title("Revenue by Product Type")
plt.xlabel("Product Type")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# product analysis(product popularity analysis)(low and underperforming products)
product_sales = df.groupby('product_detail').agg({'transaction_qty':'sum','Revenue':'sum'}).sort_values('Revenue')
print("Product sales:\n", product_sales.head(10))

# Measure revenue concentration across menu
revenue_concentration = df.groupby('product_detail')['Revenue'].sum().sort_values(ascending=False)
print("Revenue Concentration by Product:\n", revenue_concentration.head(10))

revenue_concentration.head(10).plot(kind='bar', figsize=(10,5))
plt.title("Revenue Concentration by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# low quantity sold products
low_products = df.groupby('product_detail').agg({
    'transaction_qty':'sum',
    'Revenue':'sum'
}).sort_values('transaction_qty')

print("Low Quantity Sold Products:\n", low_products.head(10))

# Ranking products by quantity sold
product_rank = product_sales.reset_index()
product_rank['rank'] = product_rank['transaction_qty'].rank(ascending=False)
print("Product Rank:\n", product_rank.head(10))

product_rank.sort_values('rank').head(10).plot(kind='bar', x='product_detail', y='transaction_qty', figsize=(10,5))
plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# revenue share by product detail
total_revenue = df['Revenue'].sum()
revenue_share = df.groupby('product_detail')['Revenue'].sum() / total_revenue * 100
print("Revenue Share by Product:\n", revenue_share.sort_values(ascending=False).head(10))

revenue_share.sort_values(ascending=False).head(10).plot(kind='pie', autopct='%1.1f%%', figsize=(6,6))
plt.title("Revenue Share by Product")
plt.xlabel("Product")
plt.show()

#comparision of product performance by volume and revenue
volume_rank = df.groupby('product_detail')['transaction_qty'].sum().rank(ascending=False)
revenue_rank = df.groupby('product_detail')['Revenue'].sum().rank(ascending=False)
comparison = pd.DataFrame({
    'volume_rank': volume_rank,
    'revenue_rank': revenue_rank
})
print("Product Performance Comparison:\n", comparison.sort_values('revenue_rank').head(10))

comparison.sort_values('revenue_rank').head(10).plot(kind='bar', figsize=(10,5))
plt.title("Product Performance Comparison (Volume vs Revenue)")
plt.xlabel("Product")
plt.ylabel("Rank")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# revenue share by category
category_share = df.groupby('product_category')['Revenue'].sum()  
plt.figure(figsize=(8,8))
category_share.plot(kind='pie',autopct='%1.1f%%',pctdistance=0.75,labels=None,startangle=90)
plt.title("Revenue Share by Category")
plt.legend(title="Product Category",labels=category_share.index,bbox_to_anchor=(1.2,1),loc="upper left")
plt.tight_layout()
plt.show()

# revenue share by product type and category
type_category = df.groupby(['product_category','product_type'])['Revenue'].sum()
print("Revenue Share by Product Type and Category:\n", type_category)


# Pareto Analysis
product_revenue = df.groupby('product_detail')['Revenue'].sum().sort_values(ascending=False)
cumulative = product_revenue.cumsum()/product_revenue.sum()*100

pareto = pd.DataFrame({
    'Revenue':product_revenue,
    'Cumulative %':cumulative
})
print('Pareto Analysis (Top 15 Products):')
print(pareto.head(15))

# Identify the products that contribute to 80% of the revenue
pareto[pareto['Cumulative %'] <= 80]

# Identify the products that contribute to the remaining 20% of the revenue
pareto[pareto['Cumulative %'] > 80]


df.to_csv("D:\\python\\unified second project\\final_Afficionado_Coffee_Roasters.csv", index=False)
