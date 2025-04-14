import pandas as pd
from cassandra.cluster import Cluster
from uuid import uuid4
from datetime import datetime

# Load CSV
df = pd.read_csv('../data/sales_100.csv')

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('sales_keyspace')

# Load Bronze
for _, row in df.iterrows():
    session.execute(
        "INSERT INTO bronze_sales (id, raw_record) VALUES (%s, %s)",
        (uuid4(), row.to_json())
    )

# Load Silver
for _, row in df.iterrows():
    session.execute("""
        INSERT INTO silver_sales (order_id, customer_name, region, product, quantity, price, order_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        uuid4(),
        row['Customer Name'],
        row['Region'],
        row['Product'],
        int(row['Quantity']),
        float(row['Price']),
        datetime.strptime(row['Order Date'], "%Y-%m-%d").date()
    ))

# Gold 1: Total Sales by Region
region_sales = df.groupby('Region').apply(lambda x: (x['Quantity'] * x['Price']).sum()).reset_index(name='total_sales')
for _, row in region_sales.iterrows():
    session.execute(
        "INSERT INTO gold_total_sales_by_region (region, total_sales) VALUES (%s, %s)",
        (row['Region'], float(row['total_sales']))
    )

# Gold 2: Top Customers
customer_sales = df.groupby('Customer Name').apply(lambda x: (x['Quantity'] * x['Price']).sum()).reset_index(name='total_spent')
for _, row in customer_sales.iterrows():
    session.execute(
        "INSERT INTO gold_top_customers (customer_name, total_spent) VALUES (%s, %s)",
        (row['Customer Name'], float(row['total_spent']))
    )

# Gold 3: Product Sales Summary
product_summary = df.groupby('Product').agg(
    total_quantity=('Quantity', 'sum'),
    revenue=('Price', lambda x: (x * df.loc[x.index, 'Quantity']).sum())
).reset_index()

for _, row in product_summary.iterrows():
    session.execute(
        "INSERT INTO gold_product_sales_summary (product, total_quantity, revenue) VALUES (%s, %s, %s)",
        (row['Product'], int(row['total_quantity']), float(row['revenue']))
    )