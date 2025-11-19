from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Product(Base):
    __tablename__ = "products"

    product_sku = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String)
    brand = Column(String)
    price = Column(Float)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date)
    phone = Column(String)
    email = Column(String)


class Timeframe(Base):
    __tablename__ = "timeframe"

    time_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    time_id = Column(Integer)
    amount = Column(Float)
    channel = Column(String)
    payment_type = Column(String)


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer)
    product_sku = Column(Integer)
    quantity = Column(Integer)
    unit_price = Column(Float)
    line_total = Column(Float)
