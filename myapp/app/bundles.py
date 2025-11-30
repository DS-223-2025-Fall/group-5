import streamlit as st
import pandas as pd
from itertools import combinations
from collections import Counter


def _compute_bundles(df: pd.DataFrame, tx_col: str, item_col: str, min_support: float = 0.01):
    """
    Very simple pairwise bundle mining:
    - group by transaction id
    - generate all product pairs within each transaction
    - compute support, confidence, lift for each pair
    """
    # Prepare baskets
    grouped = df.groupby(tx_col)[item_col].apply(list)

    # Count items and pairs
    item_counter = Counter()
    pair_counter = Counter()
    total_tx = len(grouped)

    for basket in grouped:
        unique_items = list(set(basket))
        for item in unique_items:
            item_counter[item] += 1
        for a, b in combinations(sorted(unique_items), 2):
            pair_counter[(a, b)] += 1

    bundles = []
    for (a, b), pair_count in pair_counter.items():
        support = pair_count / total_tx
        if support < min_support:
            continue

        count_a = item_counter[a]
        count_b = item_counter[b]

        conf_a_to_b = pair_count / count_a if count_a else 0
        conf_b_to_a = pair_count / count_b if count_b else 0
        lift = support / ((count_a / total_tx) * (count_b / total_tx)) if (count_a and count_b) else 0

        bundles.append(
            {
                "products": f"{a} + {b}",
                "support": support,
                "confidence_a_to_b": conf_a_to_b,
                "confidence_b_to_a": conf_b_to_a,
                "lift": lift,
            }
        )

    # Sort by lift descending
    bundles = sorted(bundles, key=lambda x: x["lift"], reverse=True)
    return bundles


def bundles_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Bundle Recommendations</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Bundle suggestions computed from your transaction data.'
        '</p>',
        unsafe_allow_html=True,
    )

    if "data" not in st.session_state:
        st.warning("Please upload a dataset or connect to PostgreSQL first on the **Upload** page.")
        return

    df: pd.DataFrame = st.session_state.data

    if df.empty:
        st.warning("Your dataset is empty. Please load a different table or file.")
        return

    cols = df.columns.tolist()
    tx_col = st.selectbox("Transaction ID column", cols)
    item_col = st.selectbox("Product / Item column", cols)

    # Settings from global settings, if present
    min_support_default = 0.01
    min_conf_default = 0.0
    if "settings" in st.session_state:
        s = st.session_state.settings
        min_support_default = s.get("min_support", min_support_default)
        min_conf_default = s.get("min_confidence", min_conf_default)

    min_support = st.slider(
        "Minimum support (fraction of transactions)",
        0.0,
        0.2,
        float(min_support_default),
        step=0.005,
    )

    if st.button("Generate bundles"):
        with st.spinner("Analyzing transactions and discovering bundles..."):
            try:
                bundles = _compute_bundles(df, tx_col, item_col, min_support=min_support)
                # Optionally store for Performance page
                st.session_state.bundles = bundles
            except Exception as e:
                st.error(f"Error computing bundles: {e}")
                return

        if not bundles:
            st.info("No bundles found with the current support threshold. Try lowering the minimum support.")
            return

        st.success(f"Found {len(bundles)} bundles.")

        # Show top bundles as a table
        top_n = st.slider("Number of bundles to display", 5, 50, 10)
        display_df = pd.DataFrame(bundles[:top_n])
        # filter by confidence if settings
        if min_conf_default > 0:
            display_df = display_df[
                (display_df["confidence_a_to_b"] >= min_conf_default)
                | (display_df["confidence_b_to_a"] >= min_conf_default)
            ]

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Top Bundle Candidates", unsafe_allow_html=True)
        st.dataframe(display_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # If we already have bundles from a previous run, show a quick summary
    elif "bundles" in st.session_state:
        bundles = st.session_state.bundles
        st.info(f"Last run found {len(bundles)} bundles. Click **Generate bundles** to recompute.")
