from pathlib import Path
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def build_association_rules(
    sales_csv="data/raw/sales.csv",
    products_csv="data/raw/products.csv",
    output_csv="data/raw/baseline_rules.csv",
    min_support=0.005,
):
    base = Path(__file__).parent

    df_sales = pd.read_csv(base / sales_csv)
    df_products = pd.read_csv(base / products_csv)

    df = df_sales.merge(
        df_products[["product_sku", "product_name"]],
        on="product_sku",
        how="left"
    )

    basket = (
        df.groupby(["transaction_id", "product_name"])["quantity"]
        .sum()
        .unstack()
        .fillna(0)
    )

    basket = basket > 0

    frequent = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent, metric="lift", min_threshold=1.0)

    rules = rules.sort_values("lift", ascending=False)

    (base / output_csv).parent.mkdir(parents=True, exist_ok=True)
    rules.to_csv(base / output_csv, index=False)

    print(f"Saved {len(rules)} rules to {base/output_csv}")


if __name__ == "__main__":
    build_association_rules()
