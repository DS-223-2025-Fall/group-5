import streamlit as st
import pandas as pd
import altair as alt


def dashboard_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">Overview of your connected dataset.</p>',
        unsafe_allow_html=True,
    )

    if "data" not in st.session_state:
        st.warning("Please upload a dataset or connect to PostgreSQL first on the **Upload** page.")
        return

    df: pd.DataFrame = st.session_state.data

    # ---- Basic summary cards ----
    num_rows, num_cols = df.shape
    num_numeric = len(df.select_dtypes("number").columns)
    num_categorical = len(df.select_dtypes("object").columns)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Rows")
        st.markdown(f"<h3>{num_rows:,}</h3>", unsafe_allow_html=True)
        st.caption("Total records")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Columns")
        st.markdown(f"<h3>{num_cols}</h3>", unsafe_allow_html=True)
        st.caption("Features in dataset")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Numeric columns")
        st.markdown(f"<h3>{num_numeric}</h3>", unsafe_allow_html=True)
        st.caption("Suitable for metrics & charts")
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.caption("Categorical columns")
        st.markdown(f"<h3>{num_categorical}</h3>", unsafe_allow_html=True)
        st.caption("Useful for grouping / segmentation")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")

    # ---- Chart section ----
    numeric_cols = list(df.select_dtypes("number").columns)
    cat_cols = list(df.select_dtypes("object").columns)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Quick Visual Exploration", unsafe_allow_html=True)

    if numeric_cols:
        col1, col2 = st.columns(2)

        with col1:
            metric = st.selectbox("Numeric column for distribution", numeric_cols, key="dist_col")
            chart_df = df[[metric]].dropna().reset_index().rename(columns={"index": "Record"})
            chart = (
                alt.Chart(chart_df)
                .mark_bar()
                .encode(
                    x=alt.X("Record:Q", title="Record index"),
                    y=alt.Y(f"{metric}:Q", title=metric),
                )
                .properties(height=280)
            )
            st.altair_chart(chart, use_container_width=True)

        with col2:
            if cat_cols:
                category = st.selectbox(
                    "Categorical column for counts",
                    cat_cols,
                    key="cat_col",
                )
                bar_df = (
                    df[category]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"index": category, category: "Count"})
                )
                bar_chart = (
                    alt.Chart(bar_df)
                    .mark_bar()
                    .encode(
                        x=alt.X(category, sort="-y"),
                        y="Count",
                        tooltip=[category, "Count"],
                    )
                    .properties(height=280)
                )
                st.altair_chart(bar_chart, use_container_width=True)
            else:
                st.info("No categorical columns detected for count plot.")
    else:
        st.info("No numeric columns detected to plot distributions.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Data preview ----
    st.markdown("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Data Preview", unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
