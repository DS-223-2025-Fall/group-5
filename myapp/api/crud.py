"""
CRUD operations and analytics queries for the Smart Packaging Optimizer API.

This module operates between:
- FastAPI routes (main.py / routes.py)
- SQLAlchemy ORM models (Database.models)
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from Database import models, schema


# ---------------------------------------------------
# PRODUCTS
# ---------------------------------------------------
def create_product(db: Session, product: schema.ProductCreate):
    """
    Create a new product record.

    If product_sku is None and the column is autoincrement,
    PostgreSQL will generate the ID.
    """
    data = product.dict()
    db_obj = models.Product(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_products(db: Session):
    """
    Retrieve all products.
    """
    return db.query(models.Product).all()


# ---------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------
def create_customer(db: Session, customer: schema.CustomerCreate):
    """
    Create a new customer record.
    """
    data = customer.dict()
    db_obj = models.Customer(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_customers(db: Session):
    """
    Retrieve all customers.
    """
    return db.query(models.Customer).all()


# ---------------------------------------------------
# TIMEFRAME
# ---------------------------------------------------
def create_timeframe(db: Session, tf: schema.TimeframeCreate):
    """
    Create a new timeframe record (date dimension row).
    """
    data = tf.dict()
    db_obj = models.Timeframe(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_timeframe(db: Session):
    """
    Retrieve all timeframe rows.
    """
    return db.query(models.Timeframe).all()


# ---------------------------------------------------
# TRANSACTIONS
# ---------------------------------------------------
def create_transaction(db: Session, tx: schema.TransactionCreate):
    """
    Create a new transaction header.
    """
    data = tx.dict()
    db_obj = models.Transaction(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_transactions(db: Session):
    """
    Retrieve all transactions.
    """
    return db.query(models.Transaction).all()


# ---------------------------------------------------
# SALES (LINE ITEMS)
# ---------------------------------------------------
def create_sale(db: Session, sale: schema.SaleCreate):
    """
    Create a new sale (line item) record.
    """
    data = sale.dict()
    db_obj = models.Sale(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_sales(db: Session):
    """
    Retrieve all sales (line items).
    """
    return db.query(models.Sale).all()


# ---------------------------------------------------
# ANALYTICS – Top Products by Revenue
# ---------------------------------------------------
def get_top_products(db: Session, limit: int = 10):
    """
    Computes top-N products by revenue.
    Revenue = SUM(sales.line_total).
    """

    results = (
        db.query(
            models.Product.product_sku,
            models.Product.product_name,
            func.sum(models.Sale.line_total).label("revenue"),
        )
        .join(models.Sale, models.Sale.product_sku == models.Product.product_sku)
        .group_by(
            models.Product.product_sku,
            models.Product.product_name,
        )
        .order_by(func.sum(models.Sale.line_total).desc())
        .limit(limit)
        .all()
    )

    return [
        schema.TopProduct(
            product_sku=row.product_sku,
            product_name=row.product_name,
            revenue=row.revenue,
        )
        for row in results
    ]


# ---------------------------------------------------
# BUNDLE RULES
# ---------------------------------------------------
def get_bundle_rules(db: Session, limit: int = 10):
    """
    Retrieve bundle rules sorted by lift.

    Bundle rules come from your CSV baseline_rules
    (already loaded into the bundle_rules table).
    """

    rows = (
        db.query(models.BundleRule)
        .order_by(models.BundleRule.lift.desc())
        .limit(limit)
        .all()
    )

    return [
        schema.BundleRuleOut(
            antecedents=row.antecedents,
            consequents=row.consequents,
            support=row.support,
            confidence=row.confidence,
            lift=row.lift,
        )
        for row in rows
    ]
