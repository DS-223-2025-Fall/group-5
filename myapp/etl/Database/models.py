"""
SQLAlchemy ORM models used by the ETL subsystem.

These mirror the main application tables and are used by ETL scripts
for validations, transformations and more complex DB operations.

Tables:
- products
- customers
- timeframe
- transactions
- sales
- bundle_rules
"""

from sqlalchemy import Column, Integer, String, Float, Date

from .database import Base


class Product(Base):
    """
    Product catalog entry used in ETL.

    Mirrors the `products` table structure.
    """
    __tablename__ = "products"

    product_sku = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    brand = Column(String)
    price = Column(Float)


class Customer(Base):
    """
    Customer master data used in ETL.

    Mirrors the `customers` table structure.
    """
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    phone = Column(String)
    email = Column(String)


class Timeframe(Base):
    """
    Time dimension table for ETL.

    Mirrors the `timeframe` table structure.
    """
    __tablename__ = "timeframe"

    time_id = Column(Integer, primary_key=True)
    date = Column(Date)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)


class Transaction(Base):
    """
    Transaction header table for ETL.

    Mirrors the `transactions` table structure.
    """
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    time_id = Column(Integer)
    transaction_amount = Column(Float)
    channel = Column(String)
    payment_type = Column(String)


class Sale(Base):
    """
    Sales line items table for ETL.

    Mirrors the `sales` table structure.
    """
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer)
    product_sku = Column(Integer)
    quantity = Column(Integer)
    unit_price = Column(Float)
    line_total = Column(Float)


class BundleRule(Base):
    """
    Association rules table used for bundling / recommendations.

    Mirrors the `bundle_rules` table structure used by the main API.
    """
    __tablename__ = "bundle_rules"

    id = Column(Integer, primary_key=True)
    antecedents = Column(String)
    consequents = Column(String)
    support = Column(Float)
    confidence = Column(Float)
    lift = Column(Float)
