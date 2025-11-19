from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func


def create_product(db: Session, product: schemas.ProductCreate):
    # works in both Pydantic v1 and v2
    data = product.dict()   # <— IMPORTANT: use dict(), not model_dump()
    db_product = models.Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_top_products(db: Session, limit: int = 10) -> list[schemas.TopProduct]:
    # join sales + products, aggregate revenue
    query = (
        db.query(
            models.Sale.product_sku,
            models.Product.product_name,
            func.sum(models.Sale.line_total).label("total_revenue"),
        )
        .join(models.Product, models.Sale.product_sku == models.Product.product_sku)
        .group_by(models.Sale.product_sku, models.Product.product_name)
        .order_by(func.sum(models.Sale.line_total).desc())
        .limit(limit)
    )

    rows = query.all()
    return [
        schemas.TopProduct(
            product_sku=row.product_sku,
            product_name=row.product_name,
            total_revenue=float(row.total_revenue),
        )
        for row in rows
    ]