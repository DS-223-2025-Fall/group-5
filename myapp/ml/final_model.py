from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ---------- PATHS ----------

# This file is in myapp/ml/final_model.py
ML_DIR = Path(__file__).resolve().parent
MYAPP_DIR = ML_DIR.parent
DATA_DIR = MYAPP_DIR / "etl" / "data" / "raw"

MODELS_DIR = ML_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODELS_DIR / "customer_value_model.joblib"
SEGMENTS_PATH = ML_DIR / "customer_segments.csv"


def load_raw_data():
    """Load all 5 CSVs into dataframes."""
    files = {
        "transactions": "transactions.csv",
        "timeframe": "timeframe.csv",
        "sales": "sales.csv",
        "products": "products.csv",
        "customers": "customers.csv",
    }

    data = {}
    for key, filename in files.items():
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Expected file not found: {path}")
        data[key] = pd.read_csv(path)
    return data


def build_customer_table(data: dict) -> pd.DataFrame:
    """
    Build a customer-level table with:
      - aggregated behavioral features
      - is_high_value target

    Returns a DataFrame with columns:
      customer_id, is_high_value, [feature columns...]
    """
    transactions = data["transactions"].copy()
    timeframe = data["timeframe"].copy()
    sales = data["sales"].copy()
    products = data["products"].copy()
    customers = data["customers"].copy()

    # timeframe: time_id,date,day,month,year
    timeframe["date"] = pd.to_datetime(timeframe["date"], errors="coerce")

    # Join transactions to timeframe
    tx = transactions.merge(
        timeframe[["time_id", "date"]],
        on="time_id",
        how="left",
    )

    # Join with sales: sale_id,transaction_id,product_sku,quantity,unit_price,line_total
    tx = tx.merge(
        sales[["transaction_id", "product_sku", "quantity", "line_total"]],
        on="transaction_id",
        how="left",
    )

    # Join with products: product_sku,product_name,category,brand,price
    tx = tx.merge(
        products[["product_sku", "category", "brand"]],
        on="product_sku",
        how="left",
    )

    # ---- Aggregate to customer-level features ----
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

    # Fill NaNs
    for col in [
        "num_transactions",
        "total_spent",
        "avg_transaction_amount",
        "total_quantity",
        "num_products",
        "num_categories",
    ]:
        customer_agg[col] = customer_agg[col].fillna(0)

    # Recency & lifetime
    max_date = customer_agg["last_purchase_date"].max()
    customer_agg["recency_days"] = (max_date - customer_agg["last_purchase_date"]).dt.days
    customer_agg["customer_lifetime_days"] = (
        customer_agg["last_purchase_date"] - customer_agg["first_purchase_date"]
    ).dt.days
    customer_agg["customer_lifetime_days"] = customer_agg[
        "customer_lifetime_days"
    ].fillna(0)

    # ---- Add simple demographic feature: age ----
    customers["dob"] = pd.to_datetime(customers["dob"], errors="coerce")
    customers["age_years"] = ((max_date - customers["dob"]).dt.days / 365.25)
    customers["age_years"] = customers["age_years"].replace([np.inf, -np.inf], np.nan)
    customers["age_years"] = customers["age_years"].fillna(
        customers["age_years"].median()
    )

    demo = customers[["customer_id", "age_years"]].copy()

    full = demo.merge(customer_agg, on="customer_id", how="left")

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
        if col in full.columns:
            full[col] = full[col].fillna(0)

    # ---- Define target: is_high_value (top 25% by total_spent) ----
    threshold = full["total_spent"].quantile(0.75)
    full["is_high_value"] = (full["total_spent"] >= threshold).astype(int)

    # Keep only necessary columns
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
    cols = ["customer_id", "is_high_value"] + feature_cols
    full = full[cols].copy()

    return full


def train_model(full_df: pd.DataFrame):
    """
    Train a RandomForest to predict is_high_value and save the model.
    """
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

    X = full_df[feature_cols]
    y = full_df["is_high_value"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
            )),
        ]
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n=== Validation metrics (is_high_value) ===")
    print(classification_report(y_test, y_pred))
    try:
        auc = roc_auc_score(y_test, y_proba)
        print(f"ROC–AUC: {auc:.3f}")
    except Exception as e:
        print(f"(Could not compute ROC–AUC: {e})")

    joblib.dump(
        {
            "model": model,
            "feature_cols": feature_cols,
        },
        MODEL_PATH,
    )
    print(f"\n✅ Model saved to: {MODEL_PATH}")


def score_all_customers(full_df: pd.DataFrame):
    """
    Use the trained model to score all customers and
    save customer_segments.csv with scores + segment labels.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run this script once to train."
        )

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    feature_cols = bundle["feature_cols"]

    X_all = full_df[feature_cols]
    scores = model.predict_proba(X_all)[:, 1]

    segments = pd.DataFrame(
        {
            "customer_id": full_df["customer_id"],
            "high_value_score": scores,
        }
    )

    # Segment customers based on score using fixed ranges
    segments["segment"] = pd.cut(
        segments["high_value_score"],
        bins=[-0.001, 0.33, 0.66, 1.001],  # 0–0.33, 0.33–0.66, 0.66–1
        labels=["low", "medium", "high"],
    )

    segments.to_csv(SEGMENTS_PATH, index=False)
    print(f"✅ Customer segments saved to {SEGMENTS_PATH}")


def main():
    print(f"Using data directory: {DATA_DIR}")
    data = load_raw_data()
    full_df = build_customer_table(data)

    print(f"Built customer table with {len(full_df)} rows.")
    train_model(full_df)
    score_all_customers(full_df)
    print("\n🎉 Done – model + customer_segments.csv are ready.")


if __name__ == "__main__":
    main()
