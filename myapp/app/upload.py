import streamlit as st
import pandas as pd
from db import get_db_connection, get_all_tables, load_table_data, load_all_tables, get_table_info


def upload_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Database Connection</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Connected to PostgreSQL database. All tables loaded automatically.'
        '</p>',
        unsafe_allow_html=True,
    )

    # Auto-connect and load ALL tables on page load
    if "db_connected" not in st.session_state:
        with st.spinner("Connecting to database and loading all tables..."):
            db_info = get_db_connection()
            if db_info:
                st.session_state.db_connected = True
                st.session_state.db_info = db_info
                tables = get_all_tables()
                st.session_state.available_tables = tables
                
                # AUTO-LOAD ALL TABLES
                all_tables_data = load_all_tables()
                st.session_state.all_tables_data = all_tables_data
                
                # Calculate total rows
                total_rows = sum(df.shape[0] for df in all_tables_data.values())
                st.session_state.total_rows = total_rows
                
                st.success(f"✅ Connected! Loaded {len(all_tables_data)} tables with {total_rows:,} total rows.")
            else:
                st.session_state.db_connected = False
                st.error("❌ Failed to connect to database.")
                return

    # === DATABASE STATUS CARD ===
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if st.session_state.get("db_connected", False):
        st.markdown("### 🗄️ Database Status")
        
        all_data = st.session_state.get("all_tables_data", {})
        total_rows = st.session_state.get("total_rows", 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Status**")
            st.markdown("### ✅ Connected")
        with col2:
            st.markdown("**Tables Loaded**")
            st.markdown(f"### {len(all_data)}")
        with col3:
            st.markdown("**Total Rows**")
            st.markdown(f"### {total_rows:,}")
        
        st.markdown("---")
        
        # === TABLE BROWSER ===
        st.markdown("### 📋 Browse Tables")
        
        if all_data:
            # Table selector
            selected_table = st.selectbox(
                "Select a table to view details",
                options=list(all_data.keys()),
                key="browse_table"
            )
            
            if selected_table:
                df = all_data[selected_table]
                
                # Table info metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Rows", f"{df.shape[0]:,}")
                with col2:
                    st.metric("Columns", f"{df.shape[1]}")
                with col3:
                    st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                with col4:
                    null_count = df.isnull().sum().sum()
                    st.metric("Null Values", f"{null_count:,}")
                
                # Column details
                with st.expander("📊 Column Details", expanded=True):
                    col_info = pd.DataFrame({
                        "Column": df.columns,
                        "Type": df.dtypes.astype(str).values,
                        "Non-Null": df.count().values,
                        "Null": df.isnull().sum().values,
                        "Unique": [df[col].nunique() for col in df.columns]
                    })
                    st.dataframe(col_info, use_container_width=True, hide_index=True)
                
                # Data preview
                with st.expander("👁️ Data Preview (First 20 rows)"):
                    st.dataframe(df.head(20), use_container_width=True)
                
                # REMOVED: The "Use for Analysis" button that was causing confusion
                # Data is automatically available for all screens through st.session_state.all_tables_data
        
        # === ALL TABLES OVERVIEW ===
        st.markdown("---")
        st.markdown("### 📊 All Tables Overview")
        
        overview_data = []
        for table_name, df in all_data.items():
            overview_data.append({
                "Table": table_name,
                "Rows": df.shape[0],
                "Columns": df.shape[1],
                "Memory (KB)": round(df.memory_usage(deep=True).sum() / 1024, 1)
            })
        
        overview_df = pd.DataFrame(overview_data)
        st.dataframe(overview_df, use_container_width=True, hide_index=True)
        
        # Refresh button
        if st.button("🔄 Refresh All Data"):
            # Clear cached data
            for key in ["db_connected", "all_tables_data", "available_tables", "total_rows"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Info message
        st.markdown("---")
        st.info("💡 **All tables are automatically available for Dashboard and Bundle Suggestions.** "
                "Use the navigation menu to access different features.")
    
    else:
        st.error("❌ Database not connected.")
    
    st.markdown("</div>", unsafe_allow_html=True)