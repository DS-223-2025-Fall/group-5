# Clustr API Models

Clustr uses a unified data model shared across the ETL layer, API layer, ML engine, and Streamlit application.  
This document describes all ORM (SQLAlchemy) models and Pydantic schemas used by the FastAPI backend to validate requests and structure responses.

All model definitions are located in:

- `api/Database/models.py` — SQLAlchemy ORM tables  
- `api/Database/schema.py` — Pydantic request/response models  

The goal is to ensure consistent structure across all layers of the Clustr ecosystem.

---

## 1. Product Models

Products represent individual catalog items.

### ORM Model Fields

- product_sku  
- product_name  
- category  
- brand  
- price  

### Pydantic Schemas

- **ProductBase** – shared fields  
- **ProductCreate** – used for POST requests  
- **Product** – returned in GET responses (includes `product_sku`)  

Example conceptual structure:

    Product:
      product_sku: int
      product_name: str
      category: str
      brand: str
      price: float

---

## 2. Customer Models

Customers contain demographic, segmentation, and contact details.

### ORM Model Fields

- customer_id  
- first_name  
- last_name  
- gender  
- age  
- dob  
- email  
- phone  
- city  
- income_level  
- shopping_preference  
- customer_segment  

### Pydantic Schemas

- **CustomerBase**  
- **CustomerCreate**  
- **Customer**  

`CustomerCreate` excludes `customer_id`, while `Customer` includes it.

Conceptual structure:

    Customer:
      customer_id: int
      first_name: str
      last_name: str
      gender: str
      age: int
      email: str
      city: str
      income_level: str
      shopping_preference: str
      customer_segment: str

---

## 3. Timeframe Models

Timeframe represents individual dates used for analytics and joins.

### ORM Model Fields

- time_id  
- date  
- day  
- month  
- year  

### Pydantic Schemas

- **TimeframeBase**  
- **TimeframeCreate**  
- **Timeframe**  

Example shape:

    Timeframe:
      time_id: int
      date: YYYY-MM-DD
      day: int
      month: int
      year: int

---

## 4. Transaction Models

Transactions represent purchases made by customers.

### ORM Model Fields

- transaction_id  
- customer_id  
- time_id  
- transaction_amount  
- channel  
- payment_type  

### Pydantic Schemas

- **TransactionBase**  
- **TransactionCreate**  
- **Transaction**  

Example structure:

    Transaction:
      transaction_id: int
      customer_id: int
      time_id: int
      transaction_amount: float
      channel: str
      payment_type: str

---

## 5. Sales (Line Item) Models

Sales correspond to individual products within a transaction.

### ORM Model Fields

- sale_id  
- transaction_id  
- product_sku  
- quantity  
- unit_price  
- line_total  

### Pydantic Schemas

- **SaleBase**  
- **SaleCreate**  
- **Sale**  

Conceptual structure:

    Sale:
      sale_id: int
      transaction_id: int
      product_sku: int
      quantity: int
      unit_price: float
      line_total: float

---

## 6. Association Rule Models (Bundle Rules)

Association rules represent baseline product bundles derived from market-basket analysis.

### ORM Model Fields

- rule_id  
- antecedents  
- consequents  
- support  
- confidence  
- lift  
- count_a  
- count_b  

### Pydantic Schema

- **BundleRule**  

Conceptual structure:

    BundleRule:
      rule_id: int
      antecedents: list
      consequents: list
      support: float
      confidence: float
      lift: float

These rules are served through `/api/bundles/association-rules/`.

---

## 7. ML Bundle Recommendation Models

The ML engine generates enhanced bundle recommendations.  
These are not stored in the database but returned as response objects.

### Fields Returned by the ML Model

- bundle (list of items)  
- support  
- confidence  
- lift  
- score (ML prediction score)  

Example structure:

    MLBundleRecommendation:
      bundle: list
      score: float
      confidence: float
      lift: float
      support: float

These models are used in `/api/bundles/recommendations/`.

---

## 8. Model Consistency Across Clustr

All ETL, backend, ML, and Streamlit layers use the same schema conventions:

- Consistent column names  
- Aligned data types  
- Centralized definitions  
- Safe request/response validation  
- Reusable ORM models  

This provides stability and prevents mismatches between layers.

---

## Summary

The Clustr API models define:

- how data is stored  
- how data is sent and received  
- how ML predictions are structured  

These unified models enable Clustr to operate as a coherent, reliable system across the ETL, API, ML, and front-end layers.
