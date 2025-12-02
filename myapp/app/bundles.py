import streamlit as st
import pandas as pd
from itertools import combinations
from collections import Counter


def _compute_bundles(df: pd.DataFrame, tx_col: str, item_col: str, min_support: float = 0.01):
    """Compute product bundles using association rule mining."""
    grouped = df.groupby(tx_col)[item_col].apply(list)
    
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

        bundles.append({
            "product_a": a,
            "product_b": b,
            "products": f"{a} + {b}",
            "support": round(support, 4),
            "confidence": round(max(conf_a_to_b, conf_b_to_a), 4),
            "lift": round(lift, 2),
            "co_occurrences": pair_count
        })

    return sorted(bundles, key=lambda x: x["lift"], reverse=True)


def bundles_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Bundle Suggestions</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'AI-powered bundle recommendations based on transaction patterns.'
        '</p>',
        unsafe_allow_html=True,
    )

    all_data = st.session_state.get("all_tables_data", {})
    
    if not all_data:
        st.warning("Please load data from the **Database** page first.")
        return

    # Initialize saved bundles
    if "saved_bundles" not in st.session_state:
        st.session_state.saved_bundles = []

    # Get sales data for bundle analysis
    sales_df = all_data.get("sales")
    products_df = all_data.get("products")
    
    if sales_df is None:
        st.error("Sales table not found. Bundle analysis requires sales data.")
        return

    st.markdown("### ⚙️ Analysis Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        min_support = st.slider("Minimum Support", 0.001, 0.1, 0.005, 0.001, 
                                help="Minimum fraction of transactions containing the bundle")
    with col2:
        top_n = st.slider("Show Top N Bundles", 5, 50, 20)

    if st.button("🔍 Generate Bundle Suggestions", type="primary"):
        with st.spinner("Analyzing transaction patterns..."):
            bundles = _compute_bundles(
                sales_df, 
                tx_col="transaction_id", 
                item_col="product_sku", 
                min_support=min_support
            )
            st.session_state.computed_bundles = bundles
            
        if bundles:
            st.success(f"Found {len(bundles)} potential bundles!")
        else:
            st.warning("No bundles found. Try lowering the minimum support.")

    # === DISPLAY COMPUTED BUNDLES ===
    if "computed_bundles" in st.session_state and st.session_state.computed_bundles:
        bundles = st.session_state.computed_bundles[:top_n]
        
        st.markdown("---")
        st.markdown("### 🎯 Recommended Bundles")
        
        for i, bundle in enumerate(bundles):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                
                # Get product names if available
                prod_a_name = bundle["product_a"]
                prod_b_name = bundle["product_b"]
                
                if products_df is not None:
                    prod_a_row = products_df[products_df["product_sku"] == bundle["product_a"]]
                    prod_b_row = products_df[products_df["product_sku"] == bundle["product_b"]]
                    if not prod_a_row.empty:
                        prod_a_name = prod_a_row.iloc[0]["product_name"]
                    if not prod_b_row.empty:
                        prod_b_name = prod_b_row.iloc[0]["product_name"]
                
                with col1:
                    st.markdown(f"**Bundle #{i+1}**")
                    st.markdown(f"🛍️ {prod_a_name} + {prod_b_name}")
                
                with col2:
                    st.metric("Lift", f"{bundle['lift']}x")
                
                with col3:
                    st.metric("Confidence", f"{bundle['confidence']*100:.1f}%")
                
                with col4:
                    # Check if already saved
                    is_saved = any(
                        b["products"] == bundle["products"] 
                        for b in st.session_state.saved_bundles
                    )
                    
                    if is_saved:
                        st.success("✅ Saved")
                    else:
                        if st.button("💾 Save Bundle", key=f"save_{i}"):
                            st.session_state.saved_bundles.append({
                                **bundle,
                                "product_a_name": prod_a_name,
                                "product_b_name": prod_b_name
                            })
                            st.rerun()
                
                st.markdown("---")

    # === SAVED BUNDLES SECTION ===
    st.markdown("### 📁 Saved Bundles")
    
    if st.session_state.saved_bundles:
        for i, saved in enumerate(st.session_state.saved_bundles):
            with st.expander(f"Bundle: {saved.get('product_a_name', saved['product_a'])} + {saved.get('product_b_name', saved['product_b'])}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lift Score", f"{saved['lift']}x")
                with col2:
                    st.metric("Confidence", f"{saved['confidence']*100:.1f}%")
                with col3:
                    st.metric("Co-occurrences", saved['co_occurrences'])
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🚀 Create Campaign", key=f"campaign_{i}", type="primary"):
                        st.session_state[f"show_campaign_{i}"] = True
                
                with col2:
                    if st.button("📊 View Analytics", key=f"analytics_{i}"):
                        st.info(f"Bundle appears in {saved['co_occurrences']} transactions")
                
                with col3:
                    if st.button("🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.saved_bundles.pop(i)
                        st.rerun()
                
                # Campaign creation form
                if st.session_state.get(f"show_campaign_{i}", False):
                    st.markdown("#### 📢 Create Marketing Campaign")
                    
                    campaign_name = st.text_input("Campaign Name", f"Bundle Promo - {saved.get('product_a_name', 'Product A')} & {saved.get('product_b_name', 'Product B')}", key=f"cname_{i}")
                    discount = st.slider("Bundle Discount %", 5, 50, 15, key=f"discount_{i}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        start_date = st.date_input("Start Date", key=f"start_{i}")
                    with col2:
                        end_date = st.date_input("End Date", key=f"end_{i}")
                    
                    target_audience = st.multiselect(
                        "Target Channels",
                        ["Email", "SMS", "Push Notification", "Social Media", "In-App"],
                        default=["Email"],
                        key=f"channels_{i}"
                    )
                    
                    if st.button("✅ Launch Campaign", key=f"launch_{i}", type="primary"):
                        st.success(f"🎉 Campaign '{campaign_name}' created successfully!")
                        st.balloons()
                        st.session_state[f"show_campaign_{i}"] = False
                        st.rerun()
    else:
        st.info("No bundles saved yet. Generate suggestions and save the ones you like!")

    # === BUNDLE ANALYSIS TABLE ===
    if "computed_bundles" in st.session_state and st.session_state.computed_bundles:
        st.markdown("---")
        st.markdown("### 📋 Full Bundle Analysis")
        
        bundles_df = pd.DataFrame(st.session_state.computed_bundles[:50])
        display_cols = ["products", "lift", "confidence", "support", "co_occurrences"]
        st.dataframe(bundles_df[display_cols], use_container_width=True, hide_index=True)
