# Smart Packaging Optimizer

A data-driven analytics system for identifying complementary products in the cosmetics and perfumery industry. The tool analyzes transaction data to recommend product bundles, support gift package design, and improve cross-selling efficiency.

---

## 1. Problem Definition

Bundling decisions in cosmetics retail are often based on intuition, leading to inefficient gift sets and missed revenue. Retailers lack analytical insight into which products are purchased together and cannot reliably detect profitable product combinations.

Specific challenge:

Retailers cannot quantify co-purchase patterns and therefore miss opportunities for higher basket value through optimized product bundling.

---

## 2. Solution Overview

The system analyzes historical transaction data to detect product associations and recommend bundles based on statistical measures. It uses three algorithms:

1. Association Rule Mining (Apriori)
2. Item2Vec product embeddings
3. Item-based collaborative filtering

Outputs include:

- Ranked bundle suggestions
- Support, confidence, lift metrics
- Profitability impact
- Insights by customer segment

A Streamlit dashboard provides access for marketing teams without requiring technical knowledge.

Prototype UI on Figma:  
https://layer-bonus-12629325.figma.site/  
Login: test@test.com  
Password: test

---

## 3. Architecture

Directory structure:

```
group-5/
├── docs/              # Documentation (MkDocs)
│   ├── api.md
│   ├── app.md
│   ├── etl.md
│   ├── demo.md
│   └── index.md
│
├── myapp/
│   ├── api/           # FastAPI backend
│   ├── app/           # Streamlit UI
│   ├── etl/           # Data ingestion and CSV loader
│   ├── ml/            # Analytics engine
│   ├── pgadmin_data/  # Database admin files
│   ├── docker-compose.yml
│   └── .env
│
├── ERD.png

└── Roadmap.png
```
<img width="1024" height="768" alt="image" src="https://github.com/user-attachments/assets/32ba49a0-89a6-4617-8257-4c949c58dc64" />


Technologies used:
- PostgreSQL (database)
- FastAPI (REST API)
- Streamlit (UI)
- Docker Compose (orchestration)
- MkDocs (documentation)

---

## 4. Database Schema

Tables:

- products
- customers
- transactions
- sales
- timeframe

 
<img width="791" height="771" alt="image" src="https://github.com/user-attachments/assets/428b4499-d45c-42cd-9c7f-d012e60c5480" />


---

## 5. Data Inputs

Required fields:

- product SKU, name, category, brand
- quantity, unit price
- transaction date
- customer ID (optional)
- channel and payment type (optional)

Sample datasets are located in:  
`/myapp/etl/data/raw/`

---

## 6. Running the System (Docker)

### Environment Variables

Create a `.env` file in `myapp/`:

```
DB_NAME=marketing_db
DB_USER=admin
DB_PASSWORD=admin123

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin123

DATABASE_URL=postgresql+psycopg2://admin:admin123@db:5432/marketing_db
```

### Start

Open terminal:

```
cd myapp
docker compose up --build
```

Docker will start database services, load CSV data, and launch the dashboard.

---

## 7. Application Interfaces

### Dashboard (Streamlit)

Start the application and open:

http://localhost:8501

<img width="1280" height="446" alt="image" src="https://github.com/user-attachments/assets/a820317a-f9d6-4127-9262-56116d1b8d61" />

<img width="1280" height="647" alt="image" src="https://github.com/user-attachments/assets/2d052f0c-3723-4fb7-ac10-b87545867a3a" />

<img width="1280" height="456" alt="image" src="https://github.com/user-attachments/assets/665ddb46-d852-4a13-ac72-57010b92ee45" />

<img width="1280" height="423" alt="image" src="https://github.com/user-attachments/assets/6f4197af-b983-471f-a441-d9cc190113cd" />

<img width="1280" height="582" alt="image" src="https://github.com/user-attachments/assets/f82f5351-209e-4791-95bf-a11a73d457fb" />




### API Documentation (Swagger)

http://localhost:8008/docs



### Database Interface (pgAdmin)

http://localhost:5051


## 8. Expected Outcomes

Key metrics:

- Multi-product transactions
- Average Basket Value (ABV)
- Bundle ROI
- Bundle sell-through rate
- Reduction of under-performing gift sets

Expected value:

Improved cross-selling, better assortment planning, and reduced waste through optimized gift set design.

---

## 9. Contributors

Marketing Analytics Project, AUA, 2025.

- Keema 
- norayramirkhanyan23  
- yeghiazariangor  
- lizakhachatryan

---


