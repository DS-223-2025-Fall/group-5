"""
API route definitions for the Smart Packaging Optimizer.

This file organizes all endpoints into a single APIRouter,
keeping main.py clean and modular.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from Database import schema
from Database.database import get_db


# All routes will be under /api/...
router = APIRouter(prefix="/api")


# ---------------------------------------------------
# PRODUCTS
# ---------------------------------------------------
@router.get("/products/", response_model=list[schema.Product])
def list_products(db: Session = Depends(get_db)):
    """
    List all products in the catalog.
    """
    return crud.get_products(db=db)


@router.post("/products/", response_model=schema.Product)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    return crud.create_product(db=db, product=product)


# ---------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------
@router.get("/customers/", response_model=list[schema.Customer])
def list_customers(db: Session = Depends(get_db)):
    """
    List all customers.
    """
    return crud.get_customers(db=db)


@router.post("/customers/", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer.
    """
    return crud.create_customer(db=db, customer=customer)


# ---------------------------------------------------
# TIMEFRAME
# ---------------------------------------------------
@router.get("/timeframe/", response_model=list[schema.Timeframe])
def list_timeframe(db: Session = Depends(get_db)):
    """
    List all timeframe rows (date dimension).
    """
    return crud.get_timeframe(db=db)


@router.post("/timeframe/", response_model=schema.Timeframe)
def create_timeframe(tf: schema.TimeframeCreate, db: Session = Depends(get_db)):
    """
    Create a new timeframe row.
    """
    return crud.create_timeframe(db=db, tf=tf)


# ---------------------------------------------------
# TRANSACTIONS
# ---------------------------------------------------
@router.get("/transactions/", response_model=list[schema.Transaction])
def list_transactions(db: Session = Depends(get_db)):
    """
    List all transactions (order headers).
    """
    return crud.get_transactions(db=db)


@router.post("/transactions/", response_model=schema.Transaction)
def create_transaction(tx: schema.TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a new transaction.
    """
    return crud.create_transaction(db=db, tx=tx)


# ---------------------------------------------------
# SALES
# ---------------------------------------------------
@router.get("/sales/", response_model=list[schema.Sale])
def list_sales(db: Session = Depends(get_db)):
    """
    List all sales (line items).
    """
    return crud.get_sales(db=db)


@router.post("/sales/", response_model=schema.Sale)
def create_sale(sale: schema.SaleCreate, db: Session = Depends(get_db)):
    """
    Create a new sale (line item).
    """
    return crud.create_sale(db=db, sale=sale)


# ---------------------------------------------------
# ANALYTICS — TOP PRODUCTS
# ---------------------------------------------------
@router.get("/analytics/top-products/", response_model=list[schema.TopProduct])
def analytics_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """
    Return top-N products ranked by revenue.
    """
    return crud.get_top_products(db=db, limit=limit)


# ---------------------------------------------------
# BUNDLE RULES
# ---------------------------------------------------
@router.get("/rules/", response_model=list[schema.BundleRuleOut])
def list_bundle_rules(limit: int = 10, db: Session = Depends(get_db)):
    """
    Return bundle rules sorted by lift (strongest associations first).
    """
    return crud.get_bundle_rules(db=db, limit=limit)
