CREATE TABLE IF NOT EXISTS gold_total_sales_by_region (
    region TEXT PRIMARY KEY,
    total_sales DECIMAL
);

CREATE TABLE IF NOT EXISTS gold_top_customers (
    customer_name TEXT PRIMARY KEY,
    total_spent DECIMAL
);

CREATE TABLE IF NOT EXISTS gold_product_sales_summary (
    product TEXT PRIMARY KEY,
    total_quantity INT,
    revenue DECIMAL
);