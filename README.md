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
