"""
Utility functions for loading raw CSV files into the ETL database.

Each function:
- Reads a CSV from `etl/data/raw/`.
- Writes it into a corresponding PostgreSQL table using `pandas.to_sql`.
- Replaces existing data in that table (if_exists="append").

This module is typically used for initial seeding of the database.
"""

from pathlib import Path

import pandas as pd

from .database import engine

from sqlalchemy import text


# Base directory of the ETL package and raw data folder.
BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"

def truncate_table(table_name: str) -> None:
    """
    Truncate an ETL table and reset its identity sequence.
    """
    with engine.begin() as conn:
        conn.execute(
            text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
        )
    print(f"  Truncated table {table_name}.")


def load_products():
    """
    Load product catalog data into the `products` table.
    """
    df = pd.read_csv(RAW / "products.csv")

    # Clear the table before inserting, but keep FK consistency
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))

    df.to_sql("products", engine, if_exists="append", index=False)
    print("  ✓ Loaded products.")


def load_customers(name: str = "customers.csv") -> None:
    """
    Load customer master data from CSV into the `customers` table.
    
    Expected columns in CSV:
    - customer_id, first_name, last_name, gender, age, dob, 
      phone, email, city, income_level, shopping_preference, customer_segment

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)
    
    # Verify all expected columns are present
    expected_cols = [
        'customer_id', 'first_name', 'last_name', 'gender', 'age', 'dob',
        'phone', 'email', 'city', 'income_level', 'shopping_preference', 
        'customer_segment'
    ]
    
    missing_cols = set(expected_cols) - set(df.columns)
    if missing_cols:
        print(f"  ⚠ Warning: Missing columns in customers.csv: {missing_cols}")
        print(f"  Available columns: {list(df.columns)}")
    
    # Select only columns that exist in both CSV and expected schema
    available_cols = [col for col in expected_cols if col in df.columns]
    df = df[available_cols]

    # Clear the table before loading to avoid duplicate primary keys
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE customers RESTART IDENTITY CASCADE"))

    df.to_sql("customers", engine, if_exists="append", index=False)
    print(f"  ✓ Loaded customers ({len(df)} rows).")


def load_timeframe(name: str = "timeframe.csv") -> None:
    """
    Load timeframe dimension data into the `timeframe` table.
    """
    df = pd.read_csv(RAW / name)

    # prevent duplicates
    truncate_table("timeframe")

    df.to_sql("timeframe", engine, if_exists="append", index=False)
    print(f"  ✓ Loaded timeframe ({len(df)} rows).")


def load_transactions(name: str = "transactions.csv") -> None:
    """
    Load transaction-level data into the `transactions` table.
    """
    df = pd.read_csv(RAW / name)

    # prevent duplicates
    truncate_table("transactions")

    df.to_sql("transactions", engine, if_exists="append", index=False)
    print(f"  ✓ Loaded transactions ({len(df)} rows).")


def load_sales(name: str = "sales.csv") -> None:
    """
    Load line-level sales data into the `sales` table.
    """
    df = pd.read_csv(RAW / name)

    # prevent duplicates
    truncate_table("sales")

    df.to_sql("sales", engine, if_exists="append", index=False)
    print(f"  ✓ Loaded sales ({len(df)} rows).")


def load_rules_from_csv(name: str = "baseline_rules.csv") -> None:
    """
    Load association rules from CSV into the `bundle_rules` table.

    The CSV may contain many columns (antecedent support, consequent support,
    leverage, conviction, etc.), but our DB table only has:

        - antecedents
        - consequents
        - support
        - confidence
        - lift
    """
    df = pd.read_csv(RAW / name)

    # Keep only the columns that actually exist in the DB table
    expected_cols = ["antecedents", "consequents", "support", "confidence", "lift"]
    df = df[expected_cols]

    # Clear existing data to avoid duplicates
    truncate_table("bundle_rules")

    df.to_sql("bundle_rules", engine, if_exists="append", index=False)
    print(f"  ✓ Loaded bundle_rules ({len(df)} rows).")