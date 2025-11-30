"""
Helper functions for analytical queries on the marketing database.

These helpers are used mainly by the dashboard / reporting layer and are
intentionally written with raw SQL for clarity and performance.

The module:
- Creates a standalone SQLAlchemy engine (for scripts / dashboards).
- Exposes convenience functions that return query results as mappings().
"""

import os

from sqlalchemy import create_engine, text

# -------------------------------------------------------------------
# DB connection
# -------------------------------------------------------------------
# Standalone connection string for running this module directly.
# If DATABASE_URL is not set, a local Postgres instance is assumed.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://admin:admin123@localhost:5432/marketing_db",
)

engine = create_engine(DATABASE_URL)


# -------------------------------------------------------------------
# 1) Revenue by category
# -------------------------------------------------------------------
def get_category_revenue(engine):
    """
    Compute total revenue per product category.

    Args:
        engine: SQLAlchemy engine connected to the marketing database.

    Returns:
        A list of mapping rows, each with:
            - category: product category name.
            - total_revenue: aggregated revenue for that category.
    """
    sql = """
        SELECT
            p.category,
            SUM(s.line_total) AS total_revenue
        FROM sales s
        JOIN products p
            ON p.product_sku = s.product_sku
        GROUP BY p.category
        ORDER BY total_revenue DESC;
    """

    with engine.connect() as conn:
        result = conn.execute(text(sql)).mappings().all()

    return result


# -------------------------------------------------------------------
# 2) Top customers by total spending
# -------------------------------------------------------------------
def get_top_customers(engine, limit: int = 5):
    """
    Return top customers ranked by total spending.

    Args:
        engine: SQLAlchemy engine connected to the marketing database.
        limit:  Maximum number of customers to return (default: 5).

    Returns:
        A list of mapping rows, each with:
            - customer_id: ID of the customer.
            - total_spent: total money spent across all orders.
            - num_orders: number of distinct transactions.
    """
    sql = """
        SELECT
            c.customer_id,
            SUM(s.line_total) AS total_spent,
            COUNT(DISTINCT t.transaction_id) AS num_orders
        FROM customers c
        JOIN transactions t
            ON t.customer_id = c.customer_id
        JOIN sales s
            ON s.transaction_id = t.transaction_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
        LIMIT :limit;
    """

    with engine.connect() as conn:
        result = conn.execute(text(sql), {"limit": limit}).mappings().all()

    return result


# -------------------------------------------------------------------
# Manual test
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Simple smoke test so we can run:
    #   python -m myapp.api.Database.db_helpers
    print("▶ CATEGORY REVENUE")
    print(get_category_revenue(engine))
    print("\n▶ TOP CUSTOMERS")
    print(get_top_customers(engine))
