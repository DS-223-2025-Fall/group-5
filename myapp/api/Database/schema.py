"""
Pydantic schemas for the Smart Packaging Optimizer API.
"""

from pydantic import BaseModel
from decimal import Decimal
from datetime import date


# ---------------------------------------------------
# PRODUCT
# ---------------------------------------------------
class ProductBase(BaseModel):
    product_name: str
    category: str | None = None
    brand: str | None = None
    price: Decimal


class ProductCreate(ProductBase):
    # Optional: if omitted, DB autoincrement can generate it
    product_sku: int | None = None


class Product(ProductBase):
    product_sku: int

    class Config:
        orm_mode = True


# ---------------------------------------------------
# CUSTOMER
# ---------------------------------------------------
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    dob: date | None = None
    phone: str | None = None
    email: str | None = None


class CustomerCreate(CustomerBase):
    customer_id: int   # provided manually (from CSV or ETL)


class Customer(CustomerBase):
    customer_id: int

    class Config:
        orm_mode = True


# ---------------------------------------------------
# TIMEFRAME
# ---------------------------------------------------
class TimeframeBase(BaseModel):
    date: date
    day: int
    month: int
    year: int


class TimeframeCreate(TimeframeBase):
    time_id: int


class Timeframe(TimeframeBase):
    time_id: int

    class Config:
        orm_mode = True


# ---------------------------------------------------
# TRANSACTION HEADER
# ---------------------------------------------------
class TransactionBase(BaseModel):
    customer_id: int
    time_id: int
    transaction_amount: Decimal
    channel: str | None = None
    payment_type: str | None = None


class TransactionCreate(TransactionBase):
    transaction_id: int


class Transaction(TransactionBase):
    transaction_id: int

    class Config:
        orm_mode = True


# ---------------------------------------------------
# SALES LINE ITEMS
# ---------------------------------------------------
class SaleBase(BaseModel):
    transaction_id: int
    product_sku: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class SaleCreate(SaleBase):
    sale_id: int


class Sale(SaleBase):
    sale_id: int

    class Config:
        orm_mode = True


# ---------------------------------------------------
# ANALYTICS
# ---------------------------------------------------
class TopProduct(BaseModel):
    product_sku: int
    product_name: str | None = None
    revenue: Decimal

    class Config:
        orm_mode = True


# ---------------------------------------------------
# BUNDLE RULES
# ---------------------------------------------------
class BundleRuleOut(BaseModel):
    antecedents: str
    consequents: str
    support: Decimal
    confidence: Decimal
    lift: Decimal

    class Config:
        orm_mode = True
