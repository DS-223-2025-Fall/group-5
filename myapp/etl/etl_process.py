"""
Main ETL pipeline runner for the marketing analytics project.

This module performs the following steps:

1. Creates all database tables defined in ETL ORM models.
2. Checks whether raw CSV files exist. If not, generates a full synthetic dataset
   (customers, products, transactions, sales).
3. Builds association rules using Apriori → saves into `baseline_rules.csv`.
4. Loads all CSV files into PostgreSQL using the functions in `load_data.py`.

This script acts as the entrypoint for running the full ETL workflow.
"""

from pathlib import Path

from Database.database import Base, engine
from Database.load_data import (
    load_products,
    load_customers,
    load_timeframe,
    load_transactions,
    load_sales,
    load_rules_from_csv,
)
from simulate_data import generate_data
from modeling import build_association_rules


def run():
    """
    Execute the full ETL process.

    Steps:
        - Create DB tables (if not exists)
        - Generate synthetic data if raw CSVs are missing
        - Build association rules (Apriori → baseline_rules.csv)
        - Load all CSVs into the PostgreSQL database

    Prints progress messages for each stage.
    """
    print("Creating DB tables...")
    Base.metadata.create_all(bind=engine)

    raw_dir = Path(__file__).parent / "data" / "raw"

    # STEP 1 — Data generation (if needed)
    if not any(raw_dir.glob("*.csv")):
        print("No CSV files found — generating synthetic dataset.")
        generate_data()

    # STEP 2 — Build Apriori / association rules
    print("Building association rules...")
    build_association_rules()

    # STEP 3 — Load all CSV files into PostgreSQL
    print("Loading CSVs into PostgreSQL...")
    load_products()
    load_customers()
    load_timeframe()
    load_transactions()
    load_sales()
    load_rules_from_csv()

    print("ETL job complete.")


if __name__ == "__main__":
    run()
