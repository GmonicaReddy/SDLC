#!/usr/bin/env python3
"""Load synthetic e-commerce CSV data into a SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "ecommerce.db"


TABLE_CONFIG: Dict[str, Dict[str, object]] = {
    "customers": {
        "filename": "customers.csv",
        "schema": """
            CREATE TABLE customers (
                customer_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                city TEXT,
                state TEXT,
                signup_date TEXT,
                loyalty_tier TEXT
            );
        """,
        "numeric_cols": [],
    },
    "products": {
        "filename": "products.csv",
        "schema": """
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock_qty INTEGER,
                active TEXT
            );
        """,
        "numeric_cols": ["price", "stock_qty"],
    },
    "orders": {
        "filename": "orders.csv",
        "schema": """
            CREATE TABLE orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT,
                shipping_city TEXT,
                shipping_state TEXT,
                total_amount REAL
            );
        """,
        "numeric_cols": ["total_amount"],
    },
    "order_items": {
        "filename": "order_items.csv",
        "schema": """
            CREATE TABLE order_items (
                order_item_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                line_total REAL NOT NULL
            );
        """,
        "numeric_cols": ["quantity", "unit_price", "line_total"],
    },
    "payments": {
        "filename": "payments.csv",
        "schema": """
            CREATE TABLE payments (
                payment_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                payment_date TEXT NOT NULL,
                amount REAL NOT NULL,
                method TEXT,
                status TEXT,
                transaction_id TEXT
            );
        """,
        "numeric_cols": ["amount"],
    },
}


def coerce_numeric(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Ensure numeric columns are stored as real numbers/integers."""
    for column in columns:
        if column not in df.columns:
            continue
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV from the data directory."""
    csv_path = DATA_DIR / filename
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")
    return pd.read_csv(csv_path)


def recreate_tables(conn: sqlite3.Connection) -> None:
    """Drop and recreate all tables according to TABLE_CONFIG."""
    cursor = conn.cursor()
    for table_name, config in TABLE_CONFIG.items():
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(config["schema"])  # type: ignore[arg-type]
    conn.commit()


def insert_data(conn: sqlite3.Connection) -> None:
    """Insert all CSV rows into their tables."""
    for table_name, config in TABLE_CONFIG.items():
        df = load_csv(config["filename"])  # type: ignore[arg-type]
        df = coerce_numeric(df, config["numeric_cols"])  # type: ignore[arg-type]
        df.to_sql(table_name, conn, if_exists="append", index=False)


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        recreate_tables(conn)
        insert_data(conn)

    print(f"Loaded CSV data into {DB_PATH}")


if __name__ == "__main__":
    main()

