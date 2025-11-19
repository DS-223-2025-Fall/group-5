from sqlalchemy import create_engine, text
import os

# -------------------------------------------------------------------
# DB connection
# -------------------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://admin:admin123@localhost:5432/marketing_db"
)

engine = create_engine(DATABASE_URL)


# -------------------------------------------------------------------
# 1) Revenue by category
# -------------------------------------------------------------------
def get_category_revenue(engine):
    """
    Returns total revenue per product category.
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
    Returns top customers by total spending.
    customers → transactions → sales.
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
    print("▶ CATEGORY REVENUE")
    print(get_category_revenue(engine))
    print("\n▶ TOP CUSTOMERS")
    print(get_top_customers(engine))
