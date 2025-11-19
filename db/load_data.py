import os
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Paths to CSVs (relative to this file)
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

# 🔧 CSV has "transaction_amount", DB column is "amount"
transactions_df = transactions_df.rename(columns={"transaction_amount": "amount"})

print(f"Loaded {len(customers_df)} customers from {CUSTOMERS_CSV}")
print(f"Loaded {len(products_df)} products from {PRODUCTS_CSV}")
print(f"Loaded {len(sales_df)} sales rows from {SALES_CSV}")
print(f"Loaded {len(timeframe_df)} timeframe rows from {TIMEFRAME_CSV}")
print(f"Loaded {len(transactions_df)} transactions from {TRANSACTIONS_CSV}")

# 3. DB connection
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "marketing_db"

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL, echo=False)

# 4. Load data
with engine.begin() as conn:
    # clear tables first so we can re-run script safely (respect FK order)
    conn.execute(text("""
        TRUNCATE TABLE sales,
                       transactions,
                       timeframe,
                       products,
                       customers
        RESTART IDENTITY CASCADE;
    """))

    # ---- customers ----
    conn.execute(
        text("""
            INSERT INTO customers (customer_id, first_name, last_name, dob, phone, email)
            VALUES (:customer_id, :first_name, :last_name, :dob, :phone, :email)
        """),
        customers_df.to_dict(orient="records")
    )
    print("Inserted customers.")

    # ---- products ----
    conn.execute(
        text("""
            INSERT INTO products (product_sku, product_name, category, brand, price)
            VALUES (:product_sku, :product_name, :category, :brand, :price)
        """),
        products_df.to_dict(orient="records")
    )
    print("Inserted products.")

    # ---- timeframe ----
    conn.execute(
        text("""
            INSERT INTO timeframe (time_id, date, day, month, year)
            VALUES (:time_id, :date, :day, :month, :year)
        """),
        timeframe_df.to_dict(orient="records")
    )
    print("Inserted timeframe.")

    # ---- transactions ----
    conn.execute(
        text("""
            INSERT INTO transactions
                (transaction_id, customer_id, time_id, amount, channel, payment_type)
            VALUES
                (:transaction_id, :customer_id, :time_id, :amount, :channel, :payment_type)
        """),
        transactions_df.to_dict(orient="records")
    )
    print("Inserted transactions.")

    # ---- sales ----
    conn.execute(
        text("""
            INSERT INTO sales (sale_id, transaction_id, product_sku, quantity, unit_price, line_total)
            VALUES (:sale_id, :transaction_id, :product_sku,
                    :quantity, :unit_price, :line_total)
        """),
        sales_df.to_dict(orient="records")
    )
    print("Inserted sales.")

print("✅ Data load finished.")
