"""
Main ETL pipeline runner for the marketing analytics project.

This module performs the following steps:

1. Drops and recreates all database tables to match updated schema.
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
        - Drop existing DB tables (to handle schema changes)
        - Create DB tables with new schema
        - Generate synthetic data if raw CSVs are missing
        - Build association rules (Apriori → baseline_rules.csv)
        - Load all CSVs into the PostgreSQL database

    Prints progress messages for each stage.
    """
    print("=" * 60)
    print("Starting ETL Process")
    print("=" * 60)
    
    # STEP 0 - Drop existing tables to handle schema changes
    print("\n[1/6] Dropping existing tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        print("✓ Tables dropped successfully")
    except Exception as e:
        print(f"⚠ Warning dropping tables: {e}")
        print("Continuing anyway...")
    
    # STEP 1 - Create tables with new schema
    print("\n[2/6] Creating DB tables with updated schema...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

    raw_dir = Path(__file__).parent / "data" / "raw"

    # STEP 2 – Data generation (if needed)
    print("\n[3/6] Checking for CSV files...")
    if not any(raw_dir.glob("*.csv")):
        print("⚠ No CSV files found – generating synthetic dataset...")
        generate_data()
        print("✓ Synthetic data generated")
    else:
        print("✓ CSV files found")

    # STEP 3 – Build Apriori / association rules
    print("\n[4/6] Building association rules...")
    build_association_rules()
    print("✓ Association rules built")

    # STEP 4 – Load all CSV files into PostgreSQL
    print("\n[5/6] Loading CSVs into PostgreSQL...")
    try:
        load_products()
        load_customers()
        load_timeframe()
        load_transactions()
        load_sales()
        load_rules_from_csv()
        print("✓ All data loaded successfully")
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        raise

    print("\n[6/6] ETL job complete!")
    print("=" * 60)


if __name__ == "__main__":
    run()