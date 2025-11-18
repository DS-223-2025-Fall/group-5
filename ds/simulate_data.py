import numpy as np
import pandas as pd

np.random.seed(42)

n_transactions = 3000
n_customers = 500

products = [
    ("P001", "Rose Essence Perfume", "fragrance", "Brand A", 80),
    ("P002", "Vanilla Dream Perfume", "fragrance", "Brand B", 70),
    ("P003", "Hydrating Face Serum", "skincare", "Brand C", 55),
    ("P004", "Daily Moisturizer", "skincare", "Brand C", 45),
    ("P005", "Matte Lipstick", "makeup", "Brand D", 25),
    ("P006", "Lip Gloss", "makeup", "Brand D", 22),
    ("P007", "Body Lotion", "body", "Brand E", 30),
    ("P008", "Shower Gel", "body", "Brand E", 18),
]

product_ids = [p[0] for p in products]
rows = []

for t_id in range(1, n_transactions + 1):
    customer_id = np.random.randint(1, n_customers + 1)
    basket_size = np.random.choice([1, 2, 3, 4], p=[0.4, 0.3, 0.2, 0.1])
    chosen = np.random.choice(product_ids, size=basket_size, replace=False)

    date = pd.Timestamp("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 90), unit="D"
    )

    for pid in chosen:
        sku, name, category, brand, price = [p for p in products if p[0] == pid][0]
        rows.append(
            {
                "transaction_id": t_id,
                "customer_id": customer_id,
                "product_sku": sku,
                "product_name": name,
                "category": category,
                "brand": brand,
                "price": price,
                "date": date,
                "quantity": 1,
            }
        )

df = pd.DataFrame(rows)
df.to_csv("transactions_simulated.csv", index=False)
print("Saved transactions_simulated.csv with", len(df), "rows")
