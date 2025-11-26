from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from Database import models, schema
from Database.database import engine, get_db

# Create tables if they don't exist (for dev/demo)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Packaging Optimizer API")


@app.get("/")
def root():
    return {"message": "Backend is connected to PostgreSQL 🎉"}


# -------------------- PRODUCT ENDPOINTS --------------------
@app.post("/products/", response_model=schema.Product)
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=list[schema.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)


# -------------------- ANALYTICS EXAMPLE --------------------
@app.get("/analytics/top-products", response_model=list[schema.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db=db, limit=limit)


# -------------------- BUNDLE RULES ENDPOINT --------------------
@app.get("/rules")
def rules(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returns top-N bundle rules that ETL stored in bundle_rules table.
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
