import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Import setup
CURRENT_DIR = Path(__file__).resolve().parent
MYAPP_DIR = CURRENT_DIR.parent
ML_DIR = MYAPP_DIR / "ml"

for path in [str(MYAPP_DIR), str(ML_DIR)]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from ml.ml_bundle_engine import BundleRecommendationEngine
    ML_AVAILABLE = True
except:
    try:
        from ml_bundle_engine import BundleRecommendationEngine
        ML_AVAILABLE = True
    except:
        ML_AVAILABLE = False


def load_transaction_data():
    """
    Load and prepare transaction data by joining sales and products tables.
    This creates the format needed for bundle analysis.
    """
    all_data = st.session_state.get("all_tables_data", {})
    
    # Try to get sales/transactions data
    sales_df = all_data.get("sales")
    transactions_df = all_data.get("transactions")
    products_df = all_data.get("products")
    
    if sales_df is None or products_df is None:
        return None, "Missing required tables: 'sales' and 'products'"
    
    # Join sales with products to get product names
    try:
        merged = sales_df.merge(
            products_df[['product_sku', 'product_name', 'category', 'price']],
            on='product_sku',
            how='left'
        )
        
        # Check if we have transaction_id
        if 'transaction_id' not in merged.columns:
            return None, "Missing 'transaction_id' column in sales data"
        
        return merged, None
    except Exception as e:
        return None, f"Error joining tables: {str(e)}"


def bundles_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">🎯 Bundle Recommendations</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'AI-powered product bundle suggestions to increase sales'
        '</p>',
        unsafe_allow_html=True,
    )

    # Load transaction data
    df, error = load_transaction_data()
    
    if error:
        st.error(f"❌ {error}")
        st.info("💡 **Required data structure:**\n"
                "- **sales** table with: transaction_id, product_sku\n"
                "- **products** table with: product_sku, product_name, category, price")
        return
    
    if df is None or df.empty:
        st.warning("📊 No transaction data available. Please check your database.")
        return

    # Show data info
    st.info(f"✅ Loaded {len(df)} transaction items from {df['transaction_id'].nunique()} transactions")

    # ---- Settings Section ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Recommendation Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Minimum Popularity**")
        support_pct = st.slider(
            "How often should products appear together?",
            min_value=0.01,
            max_value=5.0,
            value=0.1,
            step=0.05,
            format="%.2f%%",
            help="Lower = more bundles (includes rare combinations). Higher = fewer bundles (only popular combinations)",
            key="support_slider"
        )
        min_support = support_pct / 100.0
        st.caption(f"At least {support_pct}% of transactions")
    
    with col2:
        st.markdown("**🎯 Minimum Likelihood**")
        confidence_pct = st.slider(
            "How likely should customers buy both?",
            min_value=0,
            max_value=50,
            value=10,
            step=5,
            format="%d%%",
            help="When someone buys Product A, what's the chance they also buy Product B?",
            key="confidence_slider"
        )
        min_confidence = confidence_pct / 100.0
        st.caption(f"{confidence_pct}% chance of buying together")
    
    with col3:
        st.markdown("**📈 Number of Results**")
        top_n = st.slider(
            "How many bundle suggestions?",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help="Maximum number of bundle recommendations to show",
            key="topn_slider"
        )
        st.caption(f"Show top {top_n} bundles")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Generate Button ----
    st.markdown("")
    if st.button("🚀 Generate Bundle Recommendations", type="primary", use_container_width=True):
        if not ML_AVAILABLE:
            st.error("❌ ML engine not available. Please check installation.")
            return
        
        with st.spinner("🤖 Analyzing purchasing patterns..."):
            try:
                engine = BundleRecommendationEngine()
                
                bundles = engine.get_top_bundles(
                    df=df,
                    tx_col='transaction_id',
                    item_col='product_name',
                    top_n=top_n,
                    min_support=min_support,
                    min_confidence=min_confidence,
                    price_col='price',
                    category_col='category'
                )
                
                st.session_state.bundles = bundles
                st.session_state.bundle_settings = {
                    'support': min_support,
                    'confidence': min_confidence,
                    'top_n': top_n
                }
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                import traceback
                with st.expander("Show error details"):
                    st.code(traceback.format_exc())
                return

        if not bundles:
            st.info(f"⚠️ No bundles found with {support_pct}% popularity and {confidence_pct}% likelihood. Try lowering these values.")
            return

        st.success(f"✅ Found {len(bundles)} high-potential bundles!")
        
        # ML model status
        if bundles[0].get('ml_model_used'):
            st.info("🧠 Using trained ML model for predictions")
        else:
            st.info("📊 Using intelligent heuristic scoring")

    # ---- Display Results ----
    if "bundles" in st.session_state and st.session_state.bundles:
        bundles = st.session_state.bundles
        
        # Summary metrics
        st.markdown("")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("📦 Total Bundles", len(bundles))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            avg_prob = sum(b['success_probability'] for b in bundles) / len(bundles)
            st.metric("✨ Avg Success Rate", f"{avg_prob*100:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            high_conf = sum(1 for b in bundles if b['success_probability'] > 0.7)
            st.metric("🎯 High Confidence", high_conf)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            avg_lift = sum(b['lift'] for b in bundles) / len(bundles)
            st.metric("📈 Avg Lift", f"{avg_lift:.1f}x")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Bundle display
        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💎 Top Bundle Recommendations")
        
        # Filter
        filter_prob = st.slider(
            "Filter by minimum success rate",
            0.0, 1.0, 0.0, step=0.1,
            format="%d%%",
            key="filter_prob"
        )
        
        filtered_bundles = [b for b in bundles if b['success_probability'] >= filter_prob]
        
        if not filtered_bundles:
            st.warning("No bundles match the filter.")
        else:
            # Initialize saved bundles
            if 'saved_bundles' not in st.session_state:
                st.session_state.saved_bundles = []
            
            for i, bundle in enumerate(filtered_bundles, 1):
                success_pct = bundle['success_probability'] * 100
                
                # Badge
                if success_pct >= 70:
                    badge = "🟢 High Potential"
                elif success_pct >= 50:
                    badge = "🟡 Medium Potential"
                else:
                    badge = "⚪ Lower Potential"
                
                is_saved = any(b['products'] == bundle['products'] for b in st.session_state.saved_bundles)
                save_emoji = "✅" if is_saved else "💾"
                
                with st.expander(
                    f"{save_emoji} **#{i}** {bundle['products']} - {success_pct:.1f}% {badge}",
                    expanded=(i <= 3)
                ):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Bundle:** `{bundle['products']}`")
                        st.markdown(f"**Success Probability:** {success_pct:.1f}%")
                        st.markdown(f"**AI Score:** {bundle['recommendation_score']:.0f}/100")
                        st.progress(bundle['success_probability'])
                    
                    with col2:
                        st.markdown("**📊 Metrics:**")
                        st.markdown(f"- **Popularity:** {bundle['support']*100:.2f}%")
                        st.markdown(f"- **Lift:** {bundle['lift']:.1f}x")
                        st.markdown(f"- **Likelihood:** {bundle['confidence_a_to_b']*100:.0f}%")
                        st.markdown(f"- **Times seen:** {bundle['pair_count']}")
                    
                    if 'total_price' in bundle:
                        st.markdown(f"💰 **Bundle Price:** ${bundle['total_price']:.2f}")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if not is_saved:
                            if st.button(f"💾 Save Bundle", key=f"save_{i}", use_container_width=True):
                                st.session_state.saved_bundles.append(bundle)
                                st.success(f"✅ Saved!")
                                st.rerun()
                        else:
                            st.success("✅ Already saved")
                    
                    with col2:
                        if st.button(f"📢 Create Campaign", key=f"campaign_{i}", use_container_width=True):
                            st.session_state.campaign_bundle = bundle
                            st.session_state.current_screen = "Campaigns"
                            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Export
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export All Bundles to CSV", use_container_width=True):
                df_export = pd.DataFrame(bundles)
                csv = df_export.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "bundle_recommendations.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col2:
            if len(st.session_state.get('saved_bundles', [])) > 0:
                if st.button(f"👀 View Saved Bundles ({len(st.session_state.saved_bundles)})", use_container_width=True):
                    st.session_state.show_saved = True
                    st.rerun()
    
    # Show saved bundles section
    if st.session_state.get('show_saved', False):
        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💾 Saved Bundles")
        
        if not st.session_state.get('saved_bundles'):
            st.info("No saved bundles yet.")
        else:
            for i, bundle in enumerate(st.session_state.saved_bundles, 1):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{i}.** {bundle['products']}")
                with col2:
                    st.markdown(f"Success: {bundle['success_probability']*100:.1f}%")
                with col3:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.saved_bundles.pop(i-1)
                        st.rerun()
        
        if st.button("← Back to Recommendations"):
            st.session_state.show_saved = False
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)