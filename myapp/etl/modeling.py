"""
Association rule modeling module.

This script generates frequent itemsets and association rules using:

- Apriori (mlxtend.frequent_patterns.apriori)
- association_rules (mlxtend.frequent_patterns.association_rules)

Input:
    sales.csv        – product quantities per transaction
    products.csv     – product catalog

Process:
    1. Merge sales + product names.
    2. Convert to a transaction x product one-hot matrix.
    3. Run Apriori to get frequent itemsets.
    4. Generate association rules (lift, confidence, support).
    5. Save ranked rules to baseline_rules.csv.

Output:
    data/raw/baseline_rules.csv
"""

from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def build_association_rules(
    sales_csv="data/raw/sales.csv",
    products_csv="data/raw/products.csv",
    output_csv="data/raw/baseline_rules.csv",
    min_support=0.005,
):
    """
    Build association rules from transaction data.

    Args:
        sales_csv: Path to sales CSV file.
        products_csv: Path to product catalog CSV file.
        output_csv: Output path for generated rules.
        min_support: Minimum support threshold for Apriori.

    Steps:
        - Load sales and product catalog
        - Join product names into sales rows
        - Pivot into basket format (transaction → product indicators)
        - Run Apriori to find frequent itemsets
        - Generate rules using "lift"
        - Sort rules by lift descending
        - Save to CSV

    Returns:
        None (writes results to CSV).
    """
    base = Path(__file__).parent

    df_sales = pd.read_csv(base / sales_csv)
    df_products = pd.read_csv(base / products_csv)

    # Merge product names into sales
    df = df_sales.merge(
        df_products[["product_sku", "product_name"]],
        on="product_sku",
        how="left",
    )

    # Transaction matrix
    basket = (
        df.groupby(["transaction_id", "product_name"])["quantity"]
        .sum()
        .unstack()
        .fillna(0)
    )
    basket = basket > 0  # Convert counts to booleans

    # Frequent itemsets
    frequent = apriori(basket, min_support=min_support, use_colnames=True)

    # Generate rules
    rules = association_rules(frequent, metric="lift", min_threshold=1.0)
    rules = rules.sort_values("lift", ascending=False)

    # Save rules
    (base / output_csv).parent.mkdir(parents=True, exist_ok=True)
    rules.to_csv(base / output_csv, index=False)

    print(f"Saved {len(rules)} rules to {base / output_csv}")


if __name__ == "__main__":
    build_association_rules()
