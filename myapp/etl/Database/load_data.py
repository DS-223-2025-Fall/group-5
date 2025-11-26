import pandas as pd
from pathlib import Path
from .database import engine

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"


def load_products(name="products.csv"):
    df = pd.read_csv(RAW / name)
    df.to_sql("products", engine, if_exists="replace", index=False)
    print("Loaded products.")


def load_customers(name="customers.csv"):
    df = pd.read_csv(RAW / name)
    df.to_sql("customers", engine, if_exists="replace", index=False)
    print("Loaded customers.")


def load_timeframe(name="timeframe.csv"):
    df = pd.read_csv(RAW / name)
    df.to_sql("timeframe", engine, if_exists="replace", index=False)
    print("Loaded timeframe.")


def load_transactions(name="transactions.csv"):
    df = pd.read_csv(RAW / name)
    df.to_sql("transactions", engine, if_exists="replace", index=False)
    print("Loaded transactions.")


def load_sales(name="sales.csv"):
    df = pd.read_csv(RAW / name)
    df.to_sql("sales", engine, if_exists="replace", index=False)
    print("Loaded sales.")


def load_rules_from_csv(name="baseline_rules.csv"):
    df = pd.read_csv(RAW / name)
    df.to_sql("bundle_rules", engine, if_exists="replace", index=False)
    print("Loaded bundle_rules.")
