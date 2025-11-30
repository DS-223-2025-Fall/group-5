import streamlit as st
import pandas as pd


def performance_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Performance Analytics</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Interpret the output of your bundle mining. This is a light-weight, data-driven summary.'
        '</p>',
        unsafe_allow_html=True,
    )

    if "data" not in st.session_state:
        st.warning("Please upload a dataset or connect to PostgreSQL first on the **Upload** page.")
        return

    if "bundles" not in st.session_state or not st.session_state.bundles:
        st.info("No bundle results found yet. Go to **Bundle Suggestions** and click *Generate bundles*.")
        return

    bundles = st.session_state.bundles
    df_bundles = pd.DataFrame(bundles)

    # Basic stats
    total_bundles = len(df_bundles)
    avg_support = df_bundles["support"].mean()
    avg_lift = df_bundles["lift"].mean()
    top_lift = df_bundles["lift"].max()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Total bundles discovered")
        st.markdown(f"<h3>{total_bundles}</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Average support")
        st.markdown(f"<h3>{avg_support*100:.2f}%</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Average lift")
        st.markdown(f"<h3>{avg_lift:.2f}x</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Highest lift bundle")
        st.markdown(f"<h3>{top_lift:.2f}x</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Top 10 Bundles by Lift", unsafe_allow_html=True)
    top_df = df_bundles.sort_values("lift", ascending=False).head(10)
    st.dataframe(top_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
