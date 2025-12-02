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
    print(f"Truncated table {table_name}.")


def load_products():
    df = pd.read_csv("data/raw/products.csv")  # or your actual path

    # Clear the table before inserting, but keep FK consistency
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))

    df.to_sql("products", engine, if_exists="append", index=False)
    print("Loaded products.")


def load_customers(name: str = "customers.csv") -> None:
    """
    Load customer master data from CSV into the `customers` table.

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)

    # NEW: clear the table before loading to avoid duplicate primary keys
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE customers RESTART IDENTITY CASCADE"))

    df.to_sql("customers", engine, if_exists="append", index=False)
    print("Loaded customers.")



def load_timeframe(name: str = "timeframe.csv") -> None:
    """
    Load timeframe dimension data into the `timeframe` table.
    """
    df = pd.read_csv(RAW / name)

    # prevent duplicates
    truncate_table("timeframe")

    df.to_sql("timeframe", engine, if_exists="append", index=False)
    print("Loaded timeframe.")



def load_transactions(name: str = "transactions.csv") -> None:
    """
    Load transaction-level data into the `transactions` table.
    """
    df = pd.read_csv(RAW / name)

    # prevent duplicates
    truncate_table("transactions")

    df.to_sql("transactions", engine, if_exists="append", index=False)
    print("Loaded transactions.")


def load_sales(name: str = "sales.csv") -> None:
    """
    Load line-level sales data into the `sales` table.
    """
    df = pd.read_csv(RAW / name)

    # prevent duplicates
    truncate_table("sales")

    df.to_sql("sales", engine, if_exists="append", index=False)
    print("Loaded sales.")



def load_rules_from_csv(name: str = "baseline_rules.csv") -> None:
    """
    Load association rules from CSV into the `bundle_rules` table.
    """
    df = pd.read_csv(RAW / name)

    # (optional) any renaming you already do stays here
    # e.g. df = df.rename(columns={...})

    # prevent duplicates
    truncate_table("bundle_rules")

    df.to_sql("bundle_rules", engine, if_exists="append", index=False)
    print("Loaded bundle_rules.")
