import streamlit as st
import pandas as pd
import sqlalchemy as sa


def _load_from_postgres(host, port, dbname, user, password, table):
    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = sa.create_engine(conn_str)
    df = pd.read_sql_table(table, con=engine)
    return df


def upload_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Connect Your Data</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Upload a dataset or connect to your PostgreSQL database. '
        'All analytics will use this data only.'
        '</p>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["📁 Upload File", "🗄️ Connect PostgreSQL"])

    # ---- TAB 1: FILE UPLOAD ----
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx", "xls"],
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.session_state.data = df
                st.success(
                    f"Upload complete — loaded `{uploaded_file.name}` "
                    f"with {df.shape[0]:,} rows and {df.shape[1]} columns."
                )

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Rows", f"{df.shape[0]:,}")
                with c2:
                    st.metric("Columns", f"{df.shape[1]}")
                with c3:
                    st.metric("Previewed rows", "5")

                st.markdown("#### Data Preview")
                st.dataframe(df.head(), use_container_width=True)
            except Exception as e:
                st.error(f"Error reading file: {e}")

        else:
            st.info("Upload a CSV/XLSX file to load data into the app.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---- TAB 2: POSTGRESQL CONNECTION ----
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### PostgreSQL Connection", unsafe_allow_html=True)
        st.caption("For demo / class use only — no advanced security.")

        host = st.text_input("Host", value="localhost")
        port = st.text_input("Port", value="5432")
        dbname = st.text_input("Database name", value="postgres")
        user = st.text_input("User", value="postgres")
        password = st.text_input("Password", type="password")

        if st.button("Test connection & list tables"):
            try:
                conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
                engine = sa.create_engine(conn_str)
                inspector = sa.inspect(engine)
                tables = inspector.get_table_names()
                if not tables:
                    st.warning("Connected, but no tables found in this database.")
                else:
                    st.session_state.pg_conn_params = {
                        "host": host,
                        "port": port,
                        "dbname": dbname,
                        "user": user,
                        "password": password,
                        "tables": tables,
                    }
                    st.success("Connection successful! Select a table to load below.")
            except Exception as e:
                st.error(f"Connection failed: {e}")

        if "pg_conn_params" in st.session_state:
            params = st.session_state.pg_conn_params
            table = st.selectbox("Choose table to load", params["tables"])
            if st.button("Load table data"):
                try:
                    df = _load_from_postgres(
                        params["host"],
                        params["port"],
                        params["dbname"],
                        params["user"],
                        params["password"],
                        table,
                    )
                    st.session_state.data = df
                    st.success(
                        f"Loaded table `{table}` with {df.shape[0]:,} rows and {df.shape[1]} columns."
                    )
                    st.markdown("#### Data Preview")
                    st.dataframe(df.head(), use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading table: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---- DATA STATUS ----
    st.markdown("")
    if "data" in st.session_state:
        st.success("✅ Data is loaded and available to Dashboard, Bundles, and Performance pages.")
        if st.button("Clear current data"):
            del st.session_state["data"]
            st.rerun()
    else:
        st.warning("No data loaded yet. Please upload a file or connect to PostgreSQL.")
