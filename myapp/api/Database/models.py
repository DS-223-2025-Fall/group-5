from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Product(Base):
    __tablename__ = "products"

    product_sku = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    price = Column(Float, nullable=False)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=True)          # from customers.csv (string -> date)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)


class Timeframe(Base):
    __tablename__ = "timeframe"

    time_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    time_id = Column(Integer, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    channel = Column(String, nullable=True)       # e.g. "Online", "In-store"
    payment_type = Column(String, nullable=True)  # e.g. "Card", "Cash"


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, nullable=False)
    product_sku = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)


class BundleRule(Base):
    """
    Stores association-rule output from your Apriori / Item2Vec pipeline.
    Matches baseline_rules.csv (antecedents, consequents, support, confidence, lift).
    """
    __tablename__ = "bundle_rules"

    id = Column(Integer, primary_key=True, index=True)
    antecedents = Column(String, nullable=False)
    consequents = Column(String, nullable=False)
    support = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    lift = Column(Float, nullable=False)
