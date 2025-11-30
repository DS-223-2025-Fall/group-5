"""
FastAPI application entry point for the Smart Packaging Optimizer API.

Responsibilities
----------------
- Initialize the FastAPI app.
- Create database tables on startup (for dev/demo).
- Expose product CRUD endpoints.
- Expose analytics and bundle-rule endpoints.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from Database import models, schema
from Database.database import engine, get_db

# Create tables if they don't exist (for dev/demo environments only).
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Packaging Optimizer API")


@app.get("/")
def root():
    """
    Health-check endpoint.

    Returns a simple JSON message confirming that the backend
    is up and connected to PostgreSQL.
    """
    return {"message": "Backend is connected to PostgreSQL 🎉"}


# -------------------- PRODUCT ENDPOINTS --------------------
@app.post("/products/", response_model=schema.Product)
def create_product(
    product: schema.ProductCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new product.

    Body:
        ProductCreate schema.

    Returns:
        The created product as a `schema.Product`.
    """
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=list[schema.Product])
def get_products(db: Session = Depends(get_db)):
    """
    List all products.

    Returns:
        A list of `schema.Product` objects.
    """
    return crud.get_products(db=db)


# -------------------- ANALYTICS EXAMPLE --------------------
@app.get("/analytics/top-products", response_model=list[schema.TopProduct])
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get top products ranked by revenue.

    Query params:
        limit: Maximum number of products to return (default: 10).

    Returns:
        A list of `schema.TopProduct` objects.
    """
    return crud.get_top_products(db=db, limit=limit)


# -------------------- BUNDLE RULES ENDPOINT --------------------
@app.get("/rules")
def rules(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Return top-N bundle rules stored in the `bundle_rules` table.

    Query params:
        limit: Maximum number of rules to return (default: 10).

    Returns:
        A list of dictionaries describing each rule with:
            - antecedents
            - consequents
            - support
            - confidence
            - lift
    """
    results = (
        db.query(models.BundleRule)
        .order_by(models.BundleRule.lift.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "antecedents": r.antecedents,
            "consequents": r.consequents,
            "support": r.support,
            "confidence": r.confidence,
            "lift": r.lift,
        }
        for r in results
    ]
