CREATE TABLE IF NOT EXISTS silver_sales (
    order_id UUID PRIMARY KEY,
    customer_name TEXT,
    region TEXT,
    product TEXT,
    quantity INT,
    price DECIMAL,
    order_date DATE
);