import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

CUSTOMERS_CSV    = os.path.join(DATA_DIR, "customers.csv")
PRODUCTS_CSV     = os.path.join(DATA_DIR, "products.csv")
SALES_CSV        = os.path.join(DATA_DIR, "sales.csv")
TIMEFRAME_CSV    = os.path.join(DATA_DIR, "timeframe.csv")
TRANSACTIONS_CSV = os.path.join(DATA_DIR, "transactions.csv")

# 2. Read CSVs
customers_df    = pd.read_csv(CUSTOMERS_CSV, parse_dates=["dob"])
products_df     = pd.read_csv(PRODUCTS_CSV)
sales_df        = pd.read_csv(SALES_CSV)
timeframe_df    = pd.read_csv(TIMEFRAME_CSV, parse_dates=["date"])
transactions_df = pd.read_csv(TRANSACTIONS_CSV)

# Clean column
transactions_df = transactions_df.rename(columns={"transaction_amount": "amount"})

print(f"Loaded {len(customers_df)} customers")
print(f"Loaded {len(products_df)} products")
print(f"Loaded {len(sales_df)} sales rows")
print(f"Loaded {len(timeframe_df)} timeframe rows")
print(f"Loaded {len(transactions_df)} transactions")

# 3. DB connection
DATABASE_URL = "postgresql+psycopg2://admin:admin123@127.0.0.1:5433/marketing_db"
engine = create_engine(DATABASE_URL, echo=False)

# 4. Auto-create and load tables
customers_df.to_sql("customers", engine, if_exists="replace", index=False)
products_df.to_sql("products", engine, if_exists="replace", index=False)
timeframe_df.to_sql("timeframe", engine, if_exists="replace", index=False)
transactions_df.to_sql("transactions", engine, if_exists="replace", index=False)
sales_df.to_sql("sales", engine, if_exists="replace", index=False)

print("✅ Data loaded successfully (tables created or replaced).")
