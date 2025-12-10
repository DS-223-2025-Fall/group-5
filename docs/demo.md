# Demo & Use Case

## 🎯 Project Overview

This project demonstrates how a **beauty & cosmetics retailer** can use data engineering and machine learning to identify product bundles, understand customer behavior, and design more effective marketing campaigns.

The system simulates a real retail pipeline:

- 🧼 **ETL** loads data from CSVs into PostgreSQL  
- 🗄️ **Database** stores customers, products, and transactions  
- ⚙️ **API (FastAPI)** exposes bundle logic and product data  
- 🤖 **ML Engine** computes association rules (support, confidence, lift)  
- 🎨 **Streamlit App** visualizes insights and enables campaign creation  

Everything is containerized and reproducible via Docker.

---

# 🌸 Use Case Scenario

A beauty retailer wants to know:

- Which products are often bought together?  
- Which bundles have the highest probability of success?  
- How should marketing create cross-sell campaigns?  

Our system enables the marketing team to:

1. View sales insights  
2. Explore data-driven product bundles  
3. Adjust support & confidence thresholds  
4. Create a discount or promotional campaign  
5. Review and export the campaign configuration  

---

# ▶️ Running the Demo

Start the entire system:

```bash
docker compose up --build
```

This launches:

| Service | Description |
|--------|-------------|
| **db** | PostgreSQL database |
| **etl** | Loads CSV data |
| **api** | FastAPI backend |
| **app** | Streamlit UI |
| **pgadmin** | Optional database admin tool |

When running, open:

- **Streamlit App** → http://localhost:8501  
- **API Docs** → http://localhost:8000/docs  
- **pgAdmin** → http://localhost:5050  

---

# 🧪 What the Demo Shows

## 1️⃣ Sales & Product Dashboard

The dashboard provides:

- Total revenue and transaction counts  
- Daily sales trend  
- Top-selling products  
- Category breakdown  
- Customer purchase behavior  

This helps contextualize which items drive sales volume.

---

## 2️⃣ Bundle Recommendation Engine

The ML engine uses association rule mining to extract:

- **Support** → How frequently products appear together  
- **Confidence** → How likely someone buys B after buying A  
- **Lift** → Strength of association beyond random chance  

### Interactive Controls:
- Minimum **Popularity (Support)**  
- Minimum **Likelihood (Confidence)**  
- Maximum number of bundles  
- Sorting options  
- Ability to drill into each bundle  

The dataset was intentionally designed with:

- **Strong pairs** (shampoo + conditioner)  
- **Medium pairs** (face cream + serum)  
- **Weak pairs** (perfume + lotion)  

This ensures that adjusting thresholds visibly changes results.

---

## 3️⃣ Campaign Creation Workflow

Once a bundle is selected, the user can create a targeted promotion:

### Inputs include:
- Discount type (percentage or fixed)
- Discount value
- Minimum order price
- Campaign budget
- Marketing channel (email, SMS, push)
- Customer segment:
    - High Value  
    - Medium Value  
    - New Customers  
    - At-Risk  
    - All Customers  
        - In this demo version, segmentation is **not computed automatically** and is stored only as metadata for the campaign.


The application then generates a summary card displaying:

- Selected bundle  
- Expected success probability  
- Applied discount  
- Targeted segment  
- Campaign metadata  

This simulates a real marketing decision-making tool.

---

# 🧱 System Architecture Overview

```
         +------------------------+
         |      Raw CSV Data      |
         +-----------+------------+
                     |
                     v
         +------------------------+
         |          ETL           |
         | Loads & validates data |
         +-----------+------------+
                     |
                     v
         +------------------------+
         |      PostgreSQL DB     |
         +-----------+------------+
                     |
         +-----------+-----------+
         |                       |
         v                       v
+------------------+     +---------------------+
| FastAPI Backend  |     |   Streamlit App     |
| Bundle Algorithm |     | Dashboards & UI     |
+------------------+     +---------------------+
                     |
                     v
         +------------------------+
         | ML Association Rules   |
         +------------------------+
```

---

# 🧰 Technologies Used

- **Python 3.12**  
- **Pandas / NumPy**  
- **FastAPI**  
- **Streamlit**  
- **PostgreSQL**  
- **Docker & Docker Compose**  
- **Association Rule Mining (lift, support, confidence)**  

---

# 🏁 Demo Flow Summary

A typical demonstration goes:

1. Run the system with Docker  
2. Open the Streamlit application  
3. Explore product & sales dashboard  
4. Navigate to bundle recommendations  
5. Try different support/confidence levels  
6. Select a bundle  
7. Create a campaign  
8. View campaign summary and insights  

This models a full **data-driven retail marketing workflow**.

---

# 🎉 Conclusion

The demo showcases a complete end-to-end system for product bundling analysis and campaign creation.  
It demonstrates how data engineering, machine learning, and interactive interfaces can support business decision-making in the retail sector.

