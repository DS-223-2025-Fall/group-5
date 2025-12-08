import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# Get the parent directory (myapp) - works in both Docker and local
CURRENT_DIR = Path(__file__).resolve().parent  # app folder
MYAPP_DIR = CURRENT_DIR.parent  # myapp folder
ML_DIR = MYAPP_DIR / "ml"  # ml folder

# Add to Python path
for path in [str(MYAPP_DIR), str(ML_DIR), str(CURRENT_DIR)]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Debug: print paths (remove after testing)
print(f"Current dir: {CURRENT_DIR}")
print(f"MyApp dir: {MYAPP_DIR}")
print(f"ML dir: {ML_DIR}")
print(f"ML dir exists: {ML_DIR.exists()}")
if ML_DIR.exists():
    print(f"Files in ML dir: {list(ML_DIR.glob('*.py'))}")

ML_AVAILABLE = False
try:
    # Try method 1: package import
    from ml.ml_bundle_engine import BundleRecommendationEngine
    ML_AVAILABLE = True
    print("✅ ML engine imported successfully (method 1)")
except ImportError as e1:
    print(f"Method 1 failed: {e1}")
    try:
        # Try method 2: direct import
        from ml_bundle_engine import BundleRecommendationEngine
        ML_AVAILABLE = True
        print("✅ ML engine imported successfully (method 2)")
    except ImportError as e2:
        print(f"Method 2 failed: {e2}")
        try:
            # Try method 3: absolute import
            import ml_bundle_engine
            BundleRecommendationEngine = ml_bundle_engine.BundleRecommendationEngine
            ML_AVAILABLE = True
            print("✅ ML engine imported successfully (method 3)")
        except ImportError as e3:
            print(f"Method 3 failed: {e3}")
            st.error(f"⚠️ Could not import ML bundle engine. Error: {e3}")
            st.info("💡 Make sure ml_bundle_engine.py exists in the ml/ folder")


def bundles_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Bundle Recommendations</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        '🤖 AI-powered bundle suggestions based on transaction patterns and ML predictions.'
        '</p>',
        unsafe_allow_html=True,
    )

    if "data" not in st.session_state:
        st.warning("Please load a dataset from the **Database** page first.")
        return

    df: pd.DataFrame = st.session_state.data

    if df.empty:
        st.warning("Your dataset is empty. Please load a different table.")
        return

    # ---- Configuration Section ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Configuration")
    
    cols = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        tx_col = st.selectbox("Transaction ID column", cols, key="tx_col")
        item_col = st.selectbox("Product / Item column", cols, key="item_col")
    
    with col2:
        # Optional columns for better predictions
        price_col = st.selectbox(
            "Price column (optional)", 
            ["None"] + cols, 
            key="price_col"
        )
        category_col = st.selectbox(
            "Category column (optional)", 
            ["None"] + cols, 
            key="category_col"
        )
    
    # Convert "None" to None
    price_col = None if price_col == "None" else price_col
    category_col = None if category_col == "None" else category_col
    
    st.markdown("---")
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_support = st.slider(
                "Minimum support",
                0.0001,
                0.05,
                0.001,
                step=0.0005,
                format="%.4f",
                help="Minimum fraction of transactions containing the bundle"
            )
        
        with col2:
            min_confidence = st.slider(
                "Minimum confidence",
                0.0,
                0.5,
                0.1,
                step=0.05,
                help="Minimum probability that items are bought together"
            )
        
        with col3:
            top_n = st.slider(
                "Number of bundles",
                5,
                50,
                20,
                step=5,
                help="Maximum number of bundle suggestions to display"
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Generate Bundles Button ----
    if st.button("🚀 Generate AI Bundle Recommendations", type="primary", use_container_width=True):
        if not ML_AVAILABLE:
            st.error("❌ ML engine is not available. Please check your installation.")
            return
        
        with st.spinner("🤖 Analyzing transaction patterns and predicting bundle success..."):
            try:
                # Initialize ML engine
                engine = BundleRecommendationEngine()
                
                # Get ML-powered recommendations
                bundles = engine.get_top_bundles(
                    df=df,
                    tx_col=tx_col,
                    item_col=item_col,
                    top_n=top_n,
                    min_support=min_support,
                    min_confidence=min_confidence,
                    price_col=price_col,
                    category_col=category_col
                )
                
                # Store in session
                st.session_state.bundles = bundles
                
            except Exception as e:
                st.error(f"❌ Error generating bundles: {e}")
                import traceback
                st.code(traceback.format_exc())
                return

        if not bundles:
            st.info("⚠️ No bundles found with the current thresholds. Try lowering the minimum support or confidence.")
            return

        st.success(f"✅ Found {len(bundles)} high-potential bundles!")
        
        # Show model status
        if bundles[0].get('ml_model_used'):
            st.info("🧠 Using trained ML model for predictions")
        else:
            st.info("📊 Using heuristic scoring (train a model for better predictions)")

    # ---- Display Results ----
    if "bundles" in st.session_state and st.session_state.bundles:
        bundles = st.session_state.bundles
        
        # Summary metrics
        st.markdown("")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Total Bundles", len(bundles))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            avg_prob = sum(b['success_probability'] for b in bundles) / len(bundles)
            st.metric("Avg Success Probability", f"{avg_prob*100:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            high_conf = sum(1 for b in bundles if b['success_probability'] > 0.7)
            st.metric("High Confidence Bundles", high_conf)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            avg_lift = sum(b['lift'] for b in bundles) / len(bundles)
            st.metric("Avg Lift", f"{avg_lift:.2f}x")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Bundle cards display
        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Top Bundle Recommendations")
        
        # Filter options
        col1, col2 = st.columns([2, 1])
        with col1:
            filter_prob = st.slider(
                "Filter by minimum success probability",
                0.0,
                1.0,
                0.0,
                step=0.1,
                key="filter_prob"
            )
        
        filtered_bundles = [b for b in bundles if b['success_probability'] >= filter_prob]
        
        if not filtered_bundles:
            st.warning("No bundles match the selected filters.")
        else:
            # Display as expandable cards
            for i, bundle in enumerate(filtered_bundles[:top_n], 1):
                success_pct = bundle['success_probability'] * 100
                
                # Color code by success probability
                if success_pct >= 70:
                    color = "#10b981"  # green
                    badge = "🟢 High Potential"
                elif success_pct >= 50:
                    color = "#f59e0b"  # yellow
                    badge = "🟡 Medium Potential"
                else:
                    color = "#6b7280"  # gray
                    badge = "⚪ Lower Potential"
                
                with st.expander(
                    f"**#{i}** {bundle['products']} - {success_pct:.1f}% Success Probability {badge}",
                    expanded=(i <= 3)
                ):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Bundle:** `{bundle['products']}`")
                        st.markdown(f"**Success Probability:** {success_pct:.1f}%")
                        st.markdown(f"**Recommendation Score:** {bundle['recommendation_score']:.1f}/100")
                        
                        # Progress bar for success probability
                        st.progress(bundle['success_probability'])
                    
                    with col2:
                        st.markdown("**Metrics:**")
                        st.markdown(f"- **Support:** {bundle['support']*100:.2f}%")
                        st.markdown(f"- **Lift:** {bundle['lift']:.2f}x")
                        st.markdown(f"- **Confidence:** {bundle['confidence_a_to_b']*100:.1f}%")
                        st.markdown(f"- **Occurrences:** {bundle['pair_count']}")
                    
                    # Additional info if available
                    if 'total_price' in bundle:
                        st.markdown(f"💰 **Bundle Price:** ${bundle['total_price']:.2f}")
                    
                    if 'is_cross_category' in bundle:
                        if bundle['is_cross_category']:
                            st.info("🔀 Cross-category bundle (higher discovery value)")
                        else:
                            st.info("📦 Same-category bundle (complementary products)")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"💾 Save Bundle #{i}", key=f"save_{i}"):
                            st.success(f"Bundle #{i} saved!")
                            # TODO: Implement save functionality
                    
                    with col2:
                        if st.button(f"📢 Create Campaign #{i}", key=f"campaign_{i}"):
                            st.success(f"Campaign created for Bundle #{i}!")
                            # TODO: Implement campaign creation
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Export option
        st.markdown("")
        if st.button("📥 Export All Bundles to CSV"):
            df_export = pd.DataFrame(bundles)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="ml_bundle_recommendations.csv",
                mime="text/csv"
            )
    
    elif "bundles" in st.session_state:
        st.info("Previous results available. Click 'Generate' to recompute with new settings.")