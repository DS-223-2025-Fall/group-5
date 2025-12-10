# Group 5 – Beauty Bundling Recommendation System

Welcome to the official documentation for our Group 5 project developed for the **Marketing Analytics** course.  
This site provides an overview of the entire system — from data engineering and machine learning to backend APIs and the Streamlit user interface.

Our project demonstrates how a retailer can use data to identify high-value product bundles, design targeted marketing campaigns, and explore customer behavior.

---

# 🌸 Project Summary

We simulate a **beauty & cosmetics retailer** and build a complete analytics ecosystem that supports:

- 📦 **Sales analysis & dashboards**  
- 🧮 **Machine-learning-powered bundle recommendations**  
- 📊 **Probability, lift, confidence & support calculations**  
- 💌 **Campaign creation inside the Streamlit app**  
- 🗄️ **ETL pipeline & PostgreSQL database**  
- 🔌 **FastAPI backend for all data and ML services**

Everything runs fully containerized using Docker, making the system easy to deploy and reproduce.

---

# 🧱 System Architecture

```
                 +-------------------------+
                 |        Raw CSV Data     |
                 +-------------+-----------+
                               |
                               v
                    +--------------------+
                    |        ETL         |
                    | Load & Transform   |
                    +---------+----------+
                              |
                              v
                     +-------------------+
                     |   PostgreSQL DB   |
                     +--+------------+---+
                        |            |
                        v            v
                +---------------+   +-----------------+
                |     API       |   |   Streamlit UI  |
                | (FastAPI)     |   | Dashboards, UI  |
                +-------+-------+   +-----------------+
                        |
                        v
              +------------------------+
              |  ML Bundle Engine      |
              | (Lift, Support, Conf.) |
              +------------------------+
```

---

# 🧩 Key Components

### 🚀 **ETL Pipeline**
Loads synthetic transaction data, transforms it, and stores it in PostgreSQL.

### 🔌 **API Service (FastAPI)**
Serves product data, transaction data, and bundle recommendations.

### 🤖 **ML Models**
Implements association rule mining to calculate:
- Support
- Confidence
- Lift
- Bundle success probability

### 🎨 **Streamlit App**
User interface for:
- Visual dashboards  
- Bundle recommendations  
- Campaign creation  

---

# 🔍 What You Can Explore in This Documentation

| Section | Description |
|--------|-------------|
| **Demo & Use Case** | A walkthrough of the demo scenario and features |
| **ETL Pipeline** | How data is loaded, cleaned, validated, and stored |
| **API Service** | Endpoints, payloads, and backend logic |
| **Streamlit App** | UI structure and interaction flow |
| **ML & API Models** | Bundle recommendation logic and data schemas |

Use the menu on the top to navigate through the system.

---

# 🧪 Running the Project

Run all services with:

```bash
docker compose up --build
```

Then access:

- Streamlit App → http://localhost:8501  
- API Docs → http://localhost:8000/docs  
- pgAdmin → http://localhost:5050  

Your dataset, model pipeline, and UI will be ready immediately.

---

# 🌟 About the Dataset

We generate a synthetic dataset designed specifically for cosmetics retail:

- 200 customers  
- 60 products  
- 2,500 transactions  
- Realistic bundles with **tiered strengths** (strong, medium, weak pairs)  
- Ideal for demonstrating how different support & confidence thresholds affect the results  

This allows the system to dynamically change bundle results as the user adjusts filters.

---

# 🎉 Conclusion

This documentation accompanies a complete end-to-end marketing analytics system built by Group 5.  
The project demonstrates real industry workflows: data extraction, transformation, storage, ML modeling, backend services, and frontend visualization.

Use the sidebar to explore each part of the system in depth.

