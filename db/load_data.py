import pandas as pd
from sqlalchemy import create_engine, text

# 1. Read the CSV
csv_path = r"C:\Users\пк\Desktop\group-5\db\data\transactions_simulated.csv"

df = pd.read_csv(csv_path, parse_dates=["date"])

print(f"Loaded {len(df)} rows from {csv_path}")

# 2. Create connection to Postgres (matches docker-compose.yml)
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "marketing_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 3. Load CSV into a staging table
with engine.begin() as conn:
    print("Writing data to staging_transactions table...")
    df.to_sql("staging_transactions", conn, if_exists="replace", index=False)

print("Staging table created.")

# 4. SQL steps to fill dimensions + fact table
SQL_STEPS = [
    # customers
    """
    INSERT INTO customers (customer_id)
    SELECT DISTINCT st.customer_id
    FROM staging_transactions st
    WHERE NOT EXISTS (
        SELECT 1 FROM customers c WHERE c.customer_id = st.customer_id
    );
    """,

    # products
    """
    INSERT INTO products (product_sku, product_name, category, brand, price)
    SELECT DISTINCT
        st.product_sku,
        st.product_name,
        st.category,
        st.brand,
        st.price
    FROM staging_transactions st
    WHERE NOT EXISTS (
        SELECT 1 FROM products p WHERE p.product_sku = st.product_sku
    );
    """,

    # timeframe
    """
    INSERT INTO timeframe (date, month, quarter, year)
    SELECT DISTINCT
        st.date::date AS date,
        EXTRACT(MONTH   FROM st.date)::int AS month,
        EXTRACT(QUARTER FROM st.date)::int AS quarter,
        EXTRACT(YEAR    FROM st.date)::int AS year
    FROM staging_transactions st
    WHERE NOT EXISTS (
        SELECT 1 FROM timeframe tf WHERE tf.date = st.date::date
    );
    """,

    # sales fact
    """
    INSERT INTO sales (
        transaction_id,
        customer_id,
        product_sku,
        sale_date,
        quantity,
        unit_price,
        total_price,
        time_id
    )
    SELECT
        st.transaction_id,
        st.customer_id,
        st.product_sku,
        st.date::date AS sale_date,
        st.quantity,
        st.price AS unit_price,
        st.price * st.quantity AS total_price,
        tf.time_id
    FROM staging_transactions st
    JOIN timeframe tf ON tf.date = st.date::date;
    """,
]

with engine.begin() as conn:
    for i, sql in enumerate(SQL_STEPS, start=1):
        print(f"Running step {i}...")
        conn.execute(text(sql))

print("✅ Data load finished.")
