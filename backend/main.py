from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, schemas, models   # ⬅️ relative imports
from .database import engine, get_db      # ⬅️ relative import

# Create tables if they don't exist (for dev/demo)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marketing Analytics Backend")

@app.get("/")
def root():
    return {"message": "Backend is connected to Postgres 🎉"}

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)

@app.get("/analytics/top-products", response_model=list[schemas.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db=db, limit=limit)
