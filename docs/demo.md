# Clustr Demo Guide

This demo guide explains how to run Clustr from end to end — starting the ETL pipeline, launching the backend API, opening the Streamlit app, and exploring bundle recommendations. It is designed to help developers, analysts, and reviewers quickly understand and operate the system.

---

## 1. Prerequisites

Before running Clustr, ensure that the following tools are installed:

- Python  
- PostgreSQL (or use dockerized version if configured)  
- Required Python dependencies (install via requirements file if provided)  

Additionally, verify that your database connection settings are correctly configured in environment variables or your application settings.

---

## 2. Run the ETL Pipeline

The ETL pipeline generates a full synthetic retail dataset and loads it into PostgreSQL.

From the project root, run:

    python etl/etl_process.py

This script performs the following:

1. Generates synthetic customers, products, timeframe, transactions, and sales.  
2. Saves all CSV files to `etl/data/raw/`.  
3. Creates database tables using SQLAlchemy models.  
4. Loads all CSVs into PostgreSQL.  
5. Generates association rules and loads them into the `bundle_rules` table.  

When complete, the database will contain all data required for Clustr to operate.

---

## 3. Start the FastAPI Backend

The backend exposes all API routes, including CRUD endpoints, association-rule outputs, and ML-based bundle recommendations.

Run:

    uvicorn api.main:app --reload

This will start the backend at:

    http://127.0.0.1:8000

Swagger UI (interactive documentation):

    http://127.0.0.1:8000/docs

You can use Swagger to:

- Inspect endpoints  
- Send test requests  
- View response structures  
- Validate database content  

---

## 4. Start the Streamlit Application

The Streamlit UI provides dashboards, customer insights, bundle discovery, and campaign tools.

Run:

    streamlit run app/app.py

Then open:

    http://localhost:8501

Pages available:

- **Dashboard** – visual insights on sales and customer segments  
- **Database** – browse tables loaded in PostgreSQL  
- **Bundles** – view association-rule and ML-based product bundles  
- **Campaigns** – convert bundles into marketing ideas  
- **Settings** – adjust app preferences  

This interface is designed for analysts and marketing users.

---

## 5. Explore the Database (Optional)

If using pgAdmin or another SQL tool, you may explore the generated tables:

- products  
- customers  
- timeframe  
- transactions  
- sales  
- bundle_rules  

pgAdmin (if running in Docker):

    http://localhost:5051

This is useful for verifying ETL results or validating API behavior.

---

## 6. Explore Bundle Recommendations

One of the core features of Clustr is recommending product bundles.

You can explore bundles using:

### Streamlit Bundles Page  
Provides filters for:

- gender  
- age range  
- income level  
- customer segment  
- shopping preferences  

Outputs include:

- association-rule bundles  
- ML bundle predictions (with score rankings)  

---

## 7. Full System Workflow Summary

The Clustr workflow works as follows:

1. **ETL**  
   Generates and loads all retail data into PostgreSQL.

2. **Backend (FastAPI)**  
   Serves data and provides ML-powered bundle recommendations.

3. **Frontend (Streamlit)**  
   Allows users to visualize insights and build marketing bundles.

4. **ML Engine**  
   Scores bundles and powers the recommendation system.

---


## 8. Conclusion

Clustr provides an integrated environment for:

- data generation  
- storage  
- analytics  
- machine learning  
- visualization  

This demo guide helps you navigate and operate the full system smoothly.
