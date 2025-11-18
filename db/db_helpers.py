from typing import List, Dict, Any
from sqlalchemy import create_engine, text

DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "marketing_db"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, future=True)


def get_connection():
    """Return a SQLAlchemy connection (use with context manager)."""
    return engine.connect()


def get_total_sales_per_category() -> List[Dict[str, Any]]:
    """
    Example helper:
    Returns total revenue per product category.
    """
    query = text(
        """
        SELECT p.category,
               SUM(s.total_price) AS total_revenue
        FROM sales s
        JOIN products p ON p.product_sku = s.product_sku
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
        return [dict(row) for row in rows]


def get_customer_purchase_history(customer_id: int) -> List[Dict[str, Any]]:
    """
    Example helper:
    Returns all purchases for a given customer.
    """
    query = text(
        """
        SELECT
            s.transaction_id,
            s.sale_date,
            s.quantity,
            s.unit_price,
            s.total_price,
            p.product_name,
            p.category,
            p.brand
        FROM sales s
        JOIN products p ON p.product_sku = s.product_sku
        WHERE s.customer_id = :customer_id
        ORDER BY s.sale_date;
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query, {"customer_id": customer_id}).mappings().all()
        return [dict(row) for row in rows]


def get_top_customers(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Example helper:
    Top N customers by total spend.
    """
    query = text(
        """
        SELECT
            customer_id,
            SUM(total_price) AS total_spent,
            COUNT(*) AS num_orders
        FROM sales
        GROUP BY customer_id
        ORDER BY total_spent DESC
        LIMIT :limit;
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query, {"limit": limit}).mappings().all()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    print(get_total_sales_per_category())
    print(get_top_customers(5))
