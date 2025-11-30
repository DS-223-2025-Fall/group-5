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


def load_products():
    df = pd.read_csv("data/raw/products.csv")  # or your actual path

    # Clear the table before inserting, but keep FK consistency
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))

    df.to_sql("products", engine, if_exists="append", index=False)
    print("Loaded products.")


def load_customers(name: str = "customers.csv") -> None:
    """
    Load customers from CSV into the `customers` table.

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)
    df.to_sql("customers", engine, if_exists="append", index=False)
    print("Loaded customers.")


def load_timeframe(name: str = "timeframe.csv") -> None:
    """
    Load timeframe dimension from CSV into the `timeframe` table.

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)
    df.to_sql("timeframe", engine, if_exists="append", index=False)
    print("Loaded timeframe.")


def load_transactions(name: str = "transactions.csv") -> None:
    """
    Load transactions from CSV into the `transactions` table.

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)
    df.to_sql("transactions", engine, if_exists="append", index=False)
    print("Loaded transactions.")


def load_sales(name: str = "sales.csv") -> None:
    """
    Load sales line items from CSV into the `sales` table.

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)
    df.to_sql("sales", engine, if_exists="append", index=False)
    print("Loaded sales.")


def load_rules_from_csv(name: str = "baseline_rules.csv") -> None:
    """
    Load association rules from CSV into the `bundle_rules` table.

    Args:
        name: CSV filename inside `etl/data/raw/`.
    """
    df = pd.read_csv(RAW / name)
    df.to_sql("bundle_rules", engine, if_exists="append", index=False)
    print("Loaded bundle_rules.")
