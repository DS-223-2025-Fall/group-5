# ETL Pipeline Documentation

The ETL (Extract–Transform–Load) subsystem is responsible for importing the synthetic retail dataset into PostgreSQL and preparing it for use by the API, ML engine, and Streamlit application.

This module ensures that all tables required for analysis and bundle generation are properly cleaned, structured, and available for querying.

---

# 🎯 Purpose of the ETL System

The ETL pipeline performs four main functions:

1. **Extract**  
   - Load raw CSV files from `data/raw/`

2. **Transform**  
   - Clean and standardize fields  
   - Convert date formats  
   - Ensure referential integrity  
   - Aggregate or merge where needed  
   - Validate numerical values (prices, totals, etc.)

3. **Load**  
   - Insert transformed data into PostgreSQL  
   - Overwrite or append based on configuration

4. **Prepare for Analytics**  
   - Ensure API endpoints can query data efficiently  
   - Allow ML engine to compute associations  
   - Support Streamlit dashboards

---

# 📁 Folder Structure

The ETL code for this project lives in the `myapp/etl/` package and is structured as follows:

```
myapp/
└── etl/
    ├── __init__.py
    ├── database.py
    ├── load_data.py
    ├── models.py
    ├── __pycache__/
    └── data/
        └── raw/
            ├── customers.xlsx
            ├── products.xlsx
            ├── sales.xlsx
            ├── timeframe.xlsx
            ├── transactions.xlsx
            └── baseline_rules.xlsx
```

- **database.py** – database connection / engine configuration  
- **load_data.py** – main ETL script that reads the raw files and loads them into PostgreSQL  
- **models.py** – (optional) data classes / helper models used by the ETL  
- **data/raw/** – folder with all input spreadsheets used by the ETL

---

# 📦 Raw Data Files (Inputs)

The ETL pipeline reads a set of Excel files from `myapp/etl/data/raw/`:

| File               | Description                                  |
|--------------------|----------------------------------------------|
| `customers.xlsx`   | Customer demographic info                    |
| `products.xlsx`    | Product catalog with categories and pricing  |
| `timeframe.xlsx`   | Calendar / date dimension                    |
| `transactions.xlsx`| Transaction-level order metadata             |
| `sales.xlsx`       | Line-item sales details per transaction      |
| `baseline_rules.xlsx` | Optional file with precomputed baseline bundle rules used for comparison/initialization |

> Note: in some earlier versions this dataset was stored as CSV files; in the current project version the ETL reads **Excel (.xlsx)** files from this folder.

---

## Schema Overview

### **customers.csv**
| Column | Description |
|--------|-------------|
| customer_id | Unique ID |
| first_name | Customer name |
| last_name | — |
| dob | Birth date |
| phone | Contact |
| email | — |

### **products.csv**
| Column | Description |
|--------|-------------|
| product_sku | Unique identifier |
| product_name | Name |
| category | Makeup / Skincare / Hair Care… |
| brand | Product brand |
| price | Unit price |

### **timeframe.csv**
| Column | Description |
|--------|-------------|
| time_id | Calendar ID |
| date | Date |
| day | Day number |
| month | Month |
| year | Year |

### **transactions.csv**
| Column | Description |
|--------|-------------|
| transaction_id | Unique order ID |
| customer_id | FK to customers |
| time_id | FK to timeframe |
| transaction_amount | Order total |
| channel | Online / In-store |
| payment_type | Card, PayPal, Cash… |

### **sales.csv**
| Column | Description |
|--------|-------------|
| sale_id | Line-item ID |
| transaction_id | FK to transactions |
| product_sku | FK to products |
| quantity | Qty purchased |
| unit_price | Price |
| line_total | Price × qty |

---

# ⚙️ How ETL Works

## 1️⃣ Extract Phase

The pipeline loads each CSV into a Pandas DataFrame:

```python
df = pd.read_csv(RAW / "customers.csv")
```

During extraction, the ETL performs validation:

- File exists  
- Columns match expected schema  
- Datatypes are interpretable  

If any critical file is missing, the ETL process stops immediately.

---

## 2️⃣ Transform Phase

Transformations applied include:

### ✔ Date parsing
```python
df['date'] = pd.to_datetime(df['date'])
```

### ✔ Numeric conversions
- Convert all pricing fields to `float`
- Convert quantity fields to `int`
- Validate transaction totals

### ✔ Cleaning rules
- Remove invalid rows (negative totals or quantity)
- Drop rows with missing foreign keys
- Ensure product SKUs exist before sales load

### ✔ Referential integrity checks
The ETL ensures:

- Every sale refers to an existing transaction  
- Every transaction refers to a valid customer & time_id  
- Every product_sku in sales exists in products  

If mismatches occur, ETL logs them and removes invalid rows.

---

## 3️⃣ Load Phase

Data is loaded into PostgreSQL using SQLAlchemy:

```python
df.to_sql("customers", engine, if_exists="replace", index=False)
```

### Load Order (to respect dependencies)

1. customers  
2. products  
3. timeframe  
4. transactions  
5. sales  

Tables are overwritten each time ETL runs (demo-friendly behavior).

---

# 🧪 Running the ETL

You can run ETL standalone:

```bash
docker compose up etl
```

Or run the full system:

```bash
docker compose up --build
```

If ETL is successful, you will see console logs such as:

```
[INFO] Loading customers...
[INFO] Loading products...
[INFO] Loading sales...
[INFO] ETL completed successfully.
```

---

# 🧰 Database Tables Produced

After ETL completes, PostgreSQL contains:

| Table | Purpose |
|--------|---------|
| **customers** | Customer demographics |
| **products** | Product catalog |
| **timeframe** | Time-based lookup table |
| **transactions** | Transaction-level data |
| **sales** | Line-item purchase records |

These tables support:

- Streamlit dashboards  
- API responses  
- ML model computations  

---

# 📊 ETL in the System Architecture

```
CSV Files → ETL → PostgreSQL → API → ML Engine → Streamlit App
```

The ETL component is foundational, ensuring all other modules operate on clean, validated, and consistently structured data.

---

# 🏁 Summary

The ETL pipeline:

- Ingests raw CSV data  
- Cleans and validates input  
- Enforces referential integrity  
- Loads structured tables into PostgreSQL  
- Prepares data for analytics and machine learning  

It ensures the entire beauty bundle recommendation system functions reliably and efficiently.
