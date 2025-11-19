from pydantic import BaseModel

class ProductBase(BaseModel):
    product_sku: int                 # ← int, not str
    product_name: str
    category: str | None = None
    brand: str | None = None
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    class Config:
        orm_mode = True

class TopProduct(BaseModel):
    product_sku: int
    product_name: str | None = None
    total_revenue: float
