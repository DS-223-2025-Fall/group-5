import streamlit as st
import pandas as pd
from db import get_db_connection, get_all_tables, load_table_data


def upload_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Database Connection</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Connected to PostgreSQL database. Select tables to load for analysis.'
        '</p>',
        unsafe_allow_html=True,
    )

    # Auto-connect to database on page load
    if "db_connected" not in st.session_state:
        with st.spinner("Connecting to database..."):
            db_info = get_db_connection()
            if db_info:
                st.session_state.db_connected = True
                st.session_state.db_info = db_info
                tables = get_all_tables()
                st.session_state.available_tables = tables
                st.success(f"✅ Connected to database! Found {len(tables)} tables.")
            else:
                st.session_state.db_connected = False
                st.error("❌ Failed to connect to database. Check your credentials.")
                return

    # Show connection status
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if st.session_state.get("db_connected", False):
        st.markdown("### 🗄️ Database Status")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", "✅ Connected")
        with col2:
            st.metric("Available Tables", len(st.session_state.get("available_tables", [])))
        with col3:
            if "data" in st.session_state:
                st.metric("Loaded Data", f"{st.session_state.data.shape[0]:,} rows")
            else:
                st.metric("Loaded Data", "None")
        
        st.markdown("---")
        
        # Table selection
        st.markdown("### Select Table to Load")
        
        tables = st.session_state.get("available_tables", [])
        
        if not tables:
            st.warning("No tables found in the database.")
        else:
            # Display tables as a selectbox
            selected_table = st.selectbox(
                "Choose a table to analyze",
                options=tables,
                key="selected_table"
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                load_button = st.button("Load Table Data", type="primary", use_container_width=True)
            with col2:
                if "data" in st.session_state:
                    if st.button("Clear Current Data", use_container_width=True):
                        del st.session_state["data"]
                        st.rerun()
            
            if load_button:
                with st.spinner(f"Loading data from table '{selected_table}'..."):
                    df = load_table_data(selected_table)
                    
                    if df is not None and not df.empty:
                        st.session_state.data = df
                        st.session_state.current_table = selected_table
                        st.success(
                            f"✅ Loaded table `{selected_table}` with {df.shape[0]:,} rows and {df.shape[1]} columns."
                        )
                        st.rerun()
                    else:
                        st.error(f"Failed to load data from table '{selected_table}' or table is empty.")
        
        # Show loaded data preview
        if "data" in st.session_state:
            st.markdown("---")
            st.markdown(f"### 📊 Current Data: `{st.session_state.get('current_table', 'Unknown')}`")
            
            df = st.session_state.data
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", f"{df.shape[0]:,}")
            with col2:
                st.metric("Columns", f"{df.shape[1]}")
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            st.markdown("#### Data Preview (First 10 Rows)")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Show column info
            with st.expander("📋 Column Information"):
                col_info = pd.DataFrame({
                    "Column": df.columns,
                    "Type": df.dtypes.astype(str),
                    "Non-Null Count": df.count().values,
                    "Null Count": df.isnull().sum().values
                })
                st.dataframe(col_info, use_container_width=True)
    
    else:
        st.error("❌ Database connection failed. Please check your environment variables and database status.")
        
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **Common issues:**
            - Ensure Docker containers are running: `docker-compose up -d`
            - Check database credentials in `.env` file
            - Verify database service name is 'db' in docker-compose.yml
            - Ensure PostgreSQL is accessible on port 5432
            
            **Required environment variables:**
            - `DB_USER`
            - `DB_PASSWORD`
            - `DB_HOST` (default: 'db')
            - `DB_PORT` (default: '5432')
            - `DB_NAME`
            """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Overall status indicator
    if "data" in st.session_state:
        st.success("✅ Data is loaded and available for Dashboard, Bundles, and Performance analysis.")
    else:
        st.info("ℹ️ No data loaded yet. Select a table above to begin analysis.")