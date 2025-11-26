from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Product(Base):
    __tablename__ = "products"

    product_sku = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    brand = Column(String)
    price = Column(Float)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    phone = Column(String)
    email = Column(String)


class Timeframe(Base):
    __tablename__ = "timeframe"

    time_id = Column(Integer, primary_key=True)
    date = Column(Date)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    time_id = Column(Integer)
    transaction_amount = Column(Float)
    channel = Column(String)
    payment_type = Column(String)


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer)
    product_sku = Column(Integer)
    quantity = Column(Integer)
    unit_price = Column(Float)
    line_total = Column(Float)


class BundleRule(Base):
    __tablename__ = "bundle_rules"

    id = Column(Integer, primary_key=True)
    antecedents = Column(String)
    consequents = Column(String)
    support = Column(Float)
    confidence = Column(Float)
    lift = Column(Float)
