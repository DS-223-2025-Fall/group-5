# ETL – Clustr Data Generation and Loading Pipeline

The ETL layer in Clustr is responsible for generating a synthetic retail dataset, creating the database schema, loading data into PostgreSQL, and preparing baseline association-rule bundles.

All ETL-related code is located in the `etl/` directory.

---

## 1. ETL Structure

Main components:

- `simulate_data.py` – synthetic data generator  
- `etl_process.py` – ETL orchestrator script  
- `Database/models.py` – SQLAlchemy ORM models  
- `Database/load_data.py` – CSV loading utilities  
- `data/raw/` – folder where generated CSVs are stored  

This pipeline ensures that all layers (ETL, API, ML, Streamlit UI) operate on the same clean and consistent data.

---

## 2. Synthetic Data Generation (`simulate_data.py`)

The synthetic data generator creates a realistic retail-style dataset. It produces:

- Customers  
- Products  
- Timeframe (daily dates)  
- Transactions  
- Sales line items  

All generated CSV files are stored in:

    etl/data/raw/

Typical configuration parameters inside the script include:

- number of customers  
- number of products  
- number of days  
- total number of transactions  
- maximum number of line items per transaction  

Output CSV files:

- `customers.csv`  
- `products.csv`  
- `timeframe.csv`  
- `transactions.csv`  
- `sales.csv`  

The data is internally consistent:

- Each transaction references an existing customer and a timeframe date.  
- Each sale references both a transaction and a product.  

---

## 3. Database Schema (`Database/models.py`)

The ETL layer defines ORM models using SQLAlchemy that mirror the structure used by the API layer.

Core tables:

- `products`  
- `customers`  
- `timeframe`  
- `transactions`  
- `sales`  
- `bundle_rules`  

These models are used to:

- Create tables in PostgreSQL before loading data.  
- Ensure column names and types are consistent between ETL and API.  

This shared schema design guarantees that:

- ETL can load data without schema mismatches.  
- FastAPI can query and serve the same tables directly.  

---

## 4. CSV Loading Utilities (`Database/load_data.py`)

This module contains helper functions for loading CSV files into PostgreSQL using pandas and SQLAlchemy.

Typical responsibilities:

- Open a database connection.  
- Optionally truncate a table before inserting new data.  
- Load CSV data from `data/raw/`.  
- Write data into the matching table.  

Common conceptual operations:

- Truncate a table before reloading:

      truncate_table("customers")

- Load a specific entity:

      load_customers()
      load_products()
      load_timeframe()
      load_transactions()
      load_sales()

The goal of this module is to provide a clear, reusable interface for loading each part of the dataset.

---

## 5. Baseline Association Rules

In addition to raw transactional data, Clustr needs baseline product bundles derived from classic market-basket analysis.

The ETL process:

1. Runs association-rule mining on historical transaction data.  
2. Produces an output CSV, for example: `baseline_rules.csv`.  
3. Loads the resulting rules into the `bundle_rules` table.  

Each rule typically contains:

- antecedents  
- consequents  
- support  
- confidence  
- lift  
- counts for the involved products  

---

## 6. ETL Orchestrator (`etl_process.py`)

The script `etl_process.py` coordinates all ETL steps and can be run to fully refresh the database.

High-level workflow:

1. **Create database schema**  
   - Uses SQLAlchemy models to create missing tables.

2. **Generate synthetic data**  
   - Calls `simulate_data.py` logic, if CSVs are missing or regeneration is needed.

3. **Load master and fact tables**  
   - Loads products, customers, timeframe, transactions, and sales from CSVs.

4. **Generate association rules**  
   - Runs association-rule mining over the transactional data.

5. **Load bundle rules**  
   - Inserts the resulting rules into the `bundle_rules` table.

Running this script ensures that the Clustr environment always has fresh data ready for analysis, dashboards, and ML inference.

---

## 7. Running the ETL Pipeline

A typical development workflow:

1. Make sure PostgreSQL is running and accessible.  
2. Configure the database connection string (for example, via environment variables).  
3. From the project root, run:

       python etl/etl_process.py

This will:

- Generate synthetic data (if needed).  
- Create tables (if they do not exist).  
- Load all core tables.  
- Populate the `bundle_rules` table with baseline association rules.  

Once ETL finishes:

- The FastAPI backend can query all data.  
- The Streamlit app can display dashboards and bundles.  
- The ML engine can train or infer using the loaded dataset.  

---

## 8. ETL in the Overall Clustr Architecture

The ETL layer is the foundation for the entire Clustr platform:

- It feeds the database with structured master and fact tables.  
- It prepares association-rule bundles for immediate use.  
- It ensures there is always consistent, reproducible data available for:  
  - API endpoints  
  - ML models  
  - Dashboards and segmentation views  

By separating generation, loading, and rule creation into dedicated components, Clustr maintains a clear, maintainable pipeline that can be extended with real data sources in the future.
