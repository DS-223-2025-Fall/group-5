import streamlit as st
import sqlalchemy as sa
import os

@st.cache_resource
def get_db_connection():
    """Create a cached database connection using environment variables."""
    try:
        # Get credentials from environment variables
        db_user = os.getenv("DB_USER", "admin")
        db_password = os.getenv("DB_PASSWORD", "admin123")
        db_host = os.getenv("DB_HOST", "db")  # 'db' is the service name in docker-compose
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "marketing_db")
        
        # Create connection string
        conn_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Create engine and connection
        engine = sa.create_engine(conn_str)
        conn = engine.connect()
        
        return {"connection": conn, "engine": engine}
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


def get_all_tables():
    """Get list of all tables in the database."""
    try:
        db_info = get_db_connection()
        if db_info is None:
            return []
        
        engine = db_info["engine"]
        inspector = sa.inspect(engine)
        tables = inspector.get_table_names()
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []


def load_table_data(table_name):
    """Load data from a specific table."""
    try:
        db_info = get_db_connection()
        if db_info is None:
            return None
        
        engine = db_info["engine"]
        query = f"SELECT * FROM {table_name}"
        df = sa.text(query)
        
        with engine.connect() as conn:
            import pandas as pd
            df = pd.read_sql(query, conn)
        
        return df
    except Exception as e:
        st.error(f"Error loading table '{table_name}': {e}")
        return None