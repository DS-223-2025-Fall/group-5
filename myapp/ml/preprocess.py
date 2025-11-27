import os
from pathlib import Path
from typing import Tuple, List, Dict

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# ---------- Paths ----------

# .../group-5/docs/myapp/ml/preprocess.py  -> parents[1] = myapp
MYAPP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = MYAPP_DIR / "etl" / "data"


def load_raw_data(data_dir: Path = DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load all raw CSVs used for modeling."""
    files = {
        "transactions": "transactions.csv",
        "timeframe": "timeframe.csv",
        "sales": "sales.csv",
        "products": "products.csv",
        "customers": "customers.csv",
    }

    data = {}
    for key, filename in files.items():
        path = data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Expected file not found: {path}")
        data[key] = pd.read_csv(path)
    return data


def build_customer_features(
    data: Dict[str, pd.DataFrame]
) -> Tuple[pd.DataFrame, List[str], str]:
    """
    Build a customer-level feature table and binary target.

    Target: `is_high_value` = 1 if customer's total spend is in top 25%.
    """

    transactions = data["transactions"].copy()
    timeframe = data["timeframe"].copy()
    sales = data["sales"].copy()
    products = data["products"].copy()
    customers = data["customers"].copy()

    # ---- 1. Join transactions with timeframe (to get dates) ----
    # time_id,date,day,month,year
    timeframe["date"] = pd.to_datetime(timeframe["date"])
    tx = transactions.merge(
        timeframe[["time_id", "date"]],
        on="time_id",
        how="left",
    )

    # ---- 2. Join with sales table (basket details) ----
    # sale_id,transaction_id,product_sku,quantity,unit_price,line_total
    tx = tx.merge(
        sales[["transaction_id", "product_sku", "quantity", "line_total"]],
        on="transaction_id",
        how="left",
    )

    # ---- 3. Join with products (category/brand) ----
    # product_sku,product_name,category,brand,price
    tx = tx.merge(
        products[["product_sku", "category", "brand"]],
        on="product_sku",
        how="left",
    )

    # ---- 4. Aggregate to customer level ----
    # Basic spending metrics
    customer_agg = (
        tx.groupby("customer_id")
        .agg(
            num_transactions=("transaction_id", "nunique"),
            total_spent=("transaction_amount", "sum"),
            avg_transaction_amount=("transaction_amount", "mean"),
            total_quantity=("quantity", "sum"),
            num_products=("product_sku", "nunique"),
            num_categories=("category", "nunique"),
            first_purchase_date=("date", "min"),
            last_purchase_date=("date", "max"),
        )
        .reset_index()
    )

    # Fill NaNs that come from customers with missing detail rows
    for col in [
        "num_transactions",
        "total_spent",
        "avg_transaction_amount",
        "total_quantity",
        "num_products",
        "num_categories",
    ]:
        customer_agg[col] = customer_agg[col].fillna(0)

    # Recency & duration
    max_date = customer_agg["last_purchase_date"].max()
    customer_agg["recency_days"] = (max_date - customer_agg["last_purchase_date"]).dt.days
    customer_agg["customer_lifetime_days"] = (
        customer_agg["last_purchase_date"] - customer_agg["first_purchase_date"]
    ).dt.days
    customer_agg["customer_lifetime_days"] = customer_agg[
        "customer_lifetime_days"
    ].fillna(0)

    # ---- 5. Add customer demographic features ----
    # customer_id,first_name,last_name,dob,phone,email
    customers["dob"] = pd.to_datetime(customers["dob"], errors="coerce")
    customers["age_years"] = ((max_date - customers["dob"]).dt.days / 365.25).round(1)
    customers["age_years"] = customers["age_years"].fillna(customers["age_years"].median())

    # We don't need names / contact info as features
    demo = customers[["customer_id", "age_years"]].copy()

    features = demo.merge(customer_agg, on="customer_id", how="left")

    # Customers may exist with zero transactions
    numeric_cols = [
        "num_transactions",
        "total_spent",
        "avg_transaction_amount",
        "total_quantity",
        "num_products",
        "num_categories",
        "recency_days",
        "customer_lifetime_days",
    ]
    for col in numeric_cols:
        if col in features.columns:
            features[col] = features[col].fillna(0)

    # ---- 6. Define target: high value customer ----
    # High value = top 25% by total_spent
    threshold = features["total_spent"].quantile(0.75)
    features["is_high_value"] = (features["total_spent"] >= threshold).astype(int)

    # Feature columns (everything numeric except id + target + date columns)
    feature_cols = [
        "age_years",
        "num_transactions",
        "total_spent",
        "avg_transaction_amount",
        "total_quantity",
        "num_products",
        "num_categories",
        "recency_days",
        "customer_lifetime_days",
    ]

    # Keep only one row per customer with id / target / features
    full_df = features[["customer_id", "is_high_value"] + feature_cols].copy()

    return full_df, feature_cols, "is_high_value"


def prepare_train_test(
    test_size: float = 0.2, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, List[str], pd.DataFrame]:
    """
    End-to-end helper:
      * load raw data
      * build customer table
      * split into train/test
    """
    data = load_raw_data()
    full_df, feature_cols, target_col = build_customer_features(data)

    X = full_df[feature_cols]
    y = full_df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test, feature_cols, full_df
