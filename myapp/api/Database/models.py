"""
SQLAlchemy ORM models backing the marketing analytics application.
"""

from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


# ---------------------------------------------------
# PRODUCTS
# ---------------------------------------------------
class Product(Base):
    __tablename__ = "products"

    product_sku = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    brand = Column(String, nullable=True)

    # NUMERIC(10,2)
    price = Column(DECIMAL(10, 2), nullable=False)

    # Relations
    sales = relationship("Sale", back_populates="product")


# ---------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Relations
    transactions = relationship("Transaction", back_populates="customer")


# ---------------------------------------------------
# TIMEFRAME
# ---------------------------------------------------
class Timeframe(Base):
    __tablename__ = "timeframe"

    time_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # Relations
    transactions = relationship("Transaction", back_populates="timeframe")


# ---------------------------------------------------
# TRANSACTION HEADER
# ---------------------------------------------------
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    time_id = Column(Integer, ForeignKey("timeframe.time_id"), nullable=False)

    transaction_amount = Column(DECIMAL(10, 2), nullable=False)
    channel = Column(String, nullable=True)
    payment_type = Column(String, nullable=True)

    # Relations
    customer = relationship("Customer", back_populates="transactions")
    timeframe = relationship("Timeframe", back_populates="transactions")
    sales = relationship("Sale", back_populates="transaction")


# ---------------------------------------------------
# SALES LINE ITEMS
# ---------------------------------------------------
class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.transaction_id"),
        nullable=False,
    )

    product_sku = Column(
        Integer,
        ForeignKey("products.product_sku"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    line_total = Column(DECIMAL(10, 2), nullable=False)

    # Relations
    transaction = relationship("Transaction", back_populates="sales")
    product = relationship("Product", back_populates="sales")


# ---------------------------------------------------
# BUNDLE RULES
# ---------------------------------------------------
class BundleRule(Base):
    __tablename__ = "bundle_rules"

    id = Column(Integer, primary_key=True, index=True)

    antecedents = Column(String, nullable=False)
    consequents = Column(String, nullable=False)
    support = Column(DECIMAL(10, 4), nullable=False)
    confidence = Column(DECIMAL(10, 4), nullable=False)
    lift = Column(DECIMAL(10, 4), nullable=False)
