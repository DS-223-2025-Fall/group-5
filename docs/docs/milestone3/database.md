# Milestone 3 – Database & ETL Internal Documentation

## 1. Database Overview
The project uses a shared PostgreSQL database accessed by the backend, ETL, and modeling components.  
The connection is configured via `DATABASE_URL` in the `.env` file.

## 2. Tables (ORM Models)
### products
- product_sku (PK)
- product_name
- category
- brand
- price

### customers
- customer_id (PK)
- first_name
- last_name
- dob
- phone
- email

### timeframe
- time_id (PK)
- date
- day
- month
- year

### transactions
- transaction_id (PK)
- customer_id
- time_id
- transaction_amount
- channel
- payment_type

### sales
- sale_id (PK)
- transaction_id
- product_sku
- quantity
- unit_price
- line_total

### bundle_rules
- id (PK)
- antecedents
- consequents
- support
- confidence
- lift

These tables are used for analytics such as revenue calculations and item bundling.

---

## 3. Backend Database Layer
Located in `myapp/api/Database`.

### database.py
- Creates SQLAlchemy engine  
- Defines `SessionLocal` and `Base`  
- Provides `get_db()` for FastAPI routes  

### models.py
Defines ORM models for all database tables.

### schema.py
Pydantic models for request and response validation.

### crud.py
Implements database operations:
- create/get products  
- compute top products  
- read bundle rules  

### main.py
API endpoints:
- `/products/`
- `/analytics/top-products`
- `/rules`

---

## 4. ETL Layer
Located in `etl/Database`.

### simulate_data.py
Generates synthetic CSV data:
- customers.csv  
- products.csv  
- timeframe.csv  
- transactions.csv  
- sales.csv  

### load_data.py
Loads CSVs into PostgreSQL using `to_sql()`.

### modeling.py
Builds association rules using Apriori and saves:
- baseline_rules.csv

### etl_process.py
Full pipeline:
1. Create tables  
2. Generate synthetic data (if needed)  
3. Build association rules  
4. Load all CSVs into the database

---

## 5. Component Flow
1. ETL generates or loads CSVs  
2. ETL loads data into PostgreSQL  
3. Backend queries the database  
4. API exposes analytics and rule-based recommendations  

---

## 6. Extending the Database
To add a new table:
- Update ORM models (API + ETL)
- Add schemas (if API uses it)
- Add CRUD logic (if needed)
- Update ETL generators/loaders
- Run migrations or `create_all()`

---

## 7. Summary
Milestone 3 provides:
- Complete ORM models  
- Documented backend DB interactions  
- Documented ETL pipeline  
- Synthetic data tools  
- Association rule modeling  
- Clear instructions for extending the schema  
