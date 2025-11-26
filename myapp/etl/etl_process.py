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
    print("Creating DB tables...")
    Base.metadata.create_all(bind=engine)

    raw_dir = Path(__file__).parent / "data" / "raw"

    # Generate synthetic data if missing
    if not any(raw_dir.glob("*.csv")):
        print("No CSV files found — generating synthetic dataset.")
        generate_data()

    print("Building association rules...")
    build_association_rules()

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
