from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()

# PARAMETERS
N_CUSTOMERS = 500
N_PRODUCTS = 200
N_DAYS = 365
N_TRANSACTIONS = 3000
MAX_LINES_PER_TRANSACTION = 5

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_data():
    # CUSTOMERS
    customers = []
    for cid in range(1, N_CUSTOMERS + 1):
        customers.append({
            "customer_id": cid,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=70),
            "phone": fake.unique.phone_number(),
            "email": fake.unique.email()
        })
    df_customers = pd.DataFrame(customers)

    # PRODUCTS
    categories = ["Clothing", "Shoes", "Accessories", "Electronics", "Beauty"]
    brands = ["Nike", "Adidas", "Zara", "H&M", "Samsung", "Apple"]

    products = []
    for pid in range(1, N_PRODUCTS + 1):
        products.append({
            "product_sku": pid,
            "product_name": fake.word().capitalize() + " " + fake.word().capitalize(),
            "category": random.choice(categories),
            "brand": random.choice(brands),
            "price": round(random.uniform(5, 500), 2)
        })
    df_products = pd.DataFrame(products)

    # TIMEFRAME
    start_date = datetime(2023, 1, 1)
    timeframe = []
    for i in range(N_DAYS):
        d = start_date + timedelta(days=i)
        timeframe.append({
            "time_id": i + 1,
            "date": d.date(),
            "day": d.day,
            "month": d.month,
            "year": d.year
        })
    df_timeframe = pd.DataFrame(timeframe)

    # TRANSACTIONS
    channels = ["Online", "In-store", "Mobile app"]
    payment_types = ["Credit Card", "Cash", "PayPal", "Bank Transfer"]

    transactions = []
    transaction_totals = {}

    for tid in range(1, N_TRANSACTIONS + 1):
        time_row = df_timeframe.sample(1).iloc[0]
        transactions.append({
            "transaction_id": tid,
            "customer_id": random.randint(1, N_CUSTOMERS),
            "time_id": int(time_row["time_id"]),
            "transaction_amount": 0.00,
            "channel": random.choice(channels),
            "payment_type": random.choice(payment_types)
        })
        transaction_totals[tid] = 0.0

    df_transactions = pd.DataFrame(transactions)

    # SALES
    sales = []
    sale_id = 1

    for tid in range(1, N_TRANSACTIONS + 1):
        n_lines = random.randint(1, MAX_LINES_PER_TRANSACTION)
        for _ in range(n_lines):
            product = df_products.sample(1).iloc[0]
            quantity = random.randint(1, 5)
            unit_price = float(product["price"])
            line_total = round(quantity * unit_price, 2)

            transaction_totals[tid] += line_total

            sales.append({
                "sale_id": sale_id,
                "transaction_id": tid,
                "product_sku": int(product["product_sku"]),
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "line_total": line_total
            })
            sale_id += 1

    df_sales = pd.DataFrame(sales)

    # Update totals
    df_transactions["transaction_amount"] = df_transactions["transaction_id"].map(
        lambda t: round(transaction_totals[t], 2)
    )

    # SAVE CSV FILES
    df_customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
    df_products.to_csv(OUTPUT_DIR / "products.csv", index=False)
    df_timeframe.to_csv(OUTPUT_DIR / "timeframe.csv", index=False)
    df_transactions.to_csv(OUTPUT_DIR / "transactions.csv", index=False)
    df_sales.to_csv(OUTPUT_DIR / "sales.csv", index=False)

    print(f"Generated synthetic data into {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_data()
