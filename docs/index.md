# Clustr Documentation

Clustr is an end-to-end retail intelligence platform that simulates retail environments, processes data through a structured ETL pipeline, performs association-rule and ML-driven bundle recommendations, and presents insights through a FastAPI backend and Streamlit interface.

This documentation provides a complete overview of the system, including data generation, database structures, API specifications, ML logic, and user interface features.

---

## Overview

Clustr includes the following major components:

- **ETL Layer**  
  Generates and loads synthetic retail datasets into PostgreSQL.

- **API Layer (FastAPI)**  
  Provides CRUD endpoints, analytics, and ML-based recommendations.

- **Frontend (Streamlit)**  
  An interface for dashboards, product bundles, campaigns, and database exploration.

- **ML Engine**  
  Generates predictive bundle recommendations based on customer segmentation and historical patterns.

- **Documentation (MkDocs)**  
  Full project documentation for developers and analysts.

---

## System Architecture

Clustr is composed of:

- A PostgreSQL database for structured master and fact tables  
- SQLAlchemy ORM models matching the API and ETL schemas  
- FastAPI service layer powering bundle recommendations  
- Streamlit app for business users  
- ETL pipeline to keep data consistent and reproducible  

---

## Documentation Sections

- **API** – Endpoints, schemas, example responses  
- **ETL** – Data generation and loading workflow  
- **App** – Streamlit UI and features  
- **Models** – ORM and Pydantic schemas  
- **Demo** – Step-by-step usage guide  

Each section is designed for clarity and professional readability.

