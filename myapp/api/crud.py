"""
CRUD operations and analytics queries for the Smart Packaging Optimizer API.

This module sits between:
- the API layer (FastAPI routes in main.py / routes.py)
- the database layer (SQLAlchemy models in Database.models)

Responsibilities
----------------
- Create new products.
- Fetch all products.
- Compute top products by revenue (for analytics endpoints).
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from Database import models, schema


def create_product(db: Session, product: schema.ProductCreate):
    """
    Create a new product record in the database.

    Args:
        db: SQLAlchemy database session.
        product: Pydantic model describing the product to create.

    Returns:
        The newly created `models.Product` instance.
    """
    # Works in both Pydantic v1 and v2.
    # Use dict() instead of model_dump() for compatibility.
    data = product.dict()
    db_product = models.Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session):
