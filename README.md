# SDLC – Synthetic E-commerce Data Project

This repository contains synthetic e-commerce datasets and scripts developed using the Cursor AI-assisted development environment as part of the A-SDLC exercise.

## 📌 Project Overview
- Generate 5 synthetic e-commerce data files:
  - `customers.csv`
  - `products.csv`
  - `orders.csv`
  - `order_items.csv`
  - `payments.csv`
- Ingest all data into a SQLite database using `ingest.py`.
- Execute SQL queries to join multiple tables and generate meaningful reports.

## 📂 Technologies Used
- Python (pandas, sqlite3)
- Cursor AI
- SQLite
- Git & GitHub

## 🗄 SQL Join Query Used

```sql
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    o.order_id,
    p.name AS product_name,
    oi.quantity,
    o.total_amount,
    pay.status AS payment_status
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
JOIN payments AS pay ON pay.order_id = o.order_id;



## prompts:
prompt 1:
Generate 5 synthetic e-commerce CSV files and save them inside the /data folder:

1. customers.csv  
2. products.csv  
3. orders.csv  
4. order_items.csv  
5. payments.csv  

Each file should have 20–50 rows of realistic sample data.  
Create proper headers for each file.

prompt 2:
Create a Python script named ingest.py that:

1. Creates a SQLite database named ecommerce.db  
2. Creates tables for customers, products, orders, order_items, and payments  
3. Reads each CSV file from the /data folder  
4. Inserts all rows into the database  

Use sqlite3 and pandas.  
The script should run directly using "python3 ingest.py".

prompt 3:
Write an SQL query (SQLite syntax) that joins the following tables:
- customers
- orders
- order_items
- products
- payments

Output should include:
customer_name, order_id, product_name, quantity, total_amount, payment_status.

Return the final SQL query only.

