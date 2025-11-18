import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def build_association_rules(
    input_csv: str = "transactions_simulated.csv",
    output_csv: str = "baseline_rules.csv",
    min_support: float = 0.005,   # LOWER SUPPORT
):
    df = pd.read_csv(input_csv)

    basket = (
        df.groupby(["transaction_id", "product_name"])["quantity"]
        .sum()
        .unstack()
        .fillna(0)
    )

    # use bool DataFrame (avoids the warning and works better)
    basket = basket > 0

    frequent = apriori(basket, min_support=min_support, use_colnames=True)

    rules = association_rules(frequent, metric="lift", min_threshold=1.0)
    rules = rules.sort_values("lift", ascending=False)

    rules.to_csv(output_csv, index=False)
    print(f"Saved {len(rules)} rules to {output_csv}")


if __name__ == "__main__":
    build_association_rules()
