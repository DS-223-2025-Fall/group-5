# Streamlit Application

The Streamlit app is the primary user interface of the Group 5 Beauty Bundling Recommendation System.  
It allows users (e.g., marketing managers) to explore sales insights, discover product bundles, and create promotional campaigns.

The app communicates with the FastAPI backend to retrieve data, compute bundle recommendations, and submit campaign configurations.

---

# 🎨 Application Overview

The Streamlit interface consists of three main sections:

1. **Dashboard** – sales analytics and product performance  
2. **Bundle Recommendations** – ML-powered product pairing suggestions  
3. **Campaign Creator** – discount and segmentation configuration  

Each section is designed to mimic a real-world marketing analytics workflow.

---

# 📊 1. Dashboard Page

The dashboard provides an overview of the retailer's sales, customers, and product activity.

### Key Metrics Displayed
- Total revenue  
- Number of transactions  
- Average order value  
- Number of customers  

### Interactive Visualizations
- **Daily sales trend**
- **Top-selling products**
- **Revenue by product category**
- **Customer purchase heatmaps**
- **Product-level performance metrics**

These charts help the user understand which products matter most before creating bundles or campaigns.

---

# 🔗 2. Bundle Recommendation Page

This is the core of the Streamlit app.

The page retrieves **bundle recommendation results** from the FastAPI backend, which runs an internal association rule mining algorithm.

### User Controls
The interface includes sliders and filters:

- **Minimum Popularity (Support)**
- **Minimum Likelihood (Confidence)**
- **Maximum number of bundles to return**
- **Sorting options (Lift, Support, Confidence, Price)**

The dataset was designed with **tiered bundle strengths**, so adjusting these thresholds visibly changes the recommendations.

### Bundle Cards
Each suggested bundle includes:

- Product names  
- Support, Confidence, Lift  
- Estimated success probability  
- Average bundle price  
- Popularity indicators  
- An **“Add to Campaign”** button  

Selecting a bundle passes its data to the Campaign Creator.

---

# 🎯 3. Campaign Creator Page

This page allows users to design a promotional campaign around a selected bundle.

### Campaign Configuration Inputs

#### 📌 Discount Options
- Percentage discount (e.g., 15%)  
- Fixed discount (e.g., $5 off)  
- Minimum order value  

### Customer Segmentation (UI-only)

The Streamlit app allows users to **select a customer segment** for campaign targeting.  
However, as of the current implementation, segmentation is **not computed internally** in the backend.

The segment is sent to the API as plain text and stored as part of the campaign configuration.  
Future versions of the system may include RFM scoring, churn probabilities, or behavioral clustering.


#### 📌 Campaign Metadata
- Marketing channel (Email, SMS, Push)  
- Campaign budget  
- Campaign name & description  

### Campaign Summary
After submission, the app displays:

- Selected bundle  
- Discount applied  
- Estimated uplift  
- Targeted customer segment  
- Full configuration in JSON format  

This simulates exporting or storing the campaign in a real marketing system.

---

# 🏗️ App Architecture

The Streamlit app interacts with the backend through HTTP calls:

```
Streamlit → FastAPI → PostgreSQL → ML Engine → Response
```

### Example API Request (Bundle Recommendations)

```python
response = requests.post(
    "http://api:8000/bundles",
    json={
        "min_support": support,
        "min_confidence": confidence,
        "max_results": limit
    }
)
```

### Example API Response

```json
{
  "bundle": ["Shampoo", "Conditioner"],
  "support": 0.18,
  "confidence": 0.62,
  "lift": 2.4,
  "success_probability": 0.73
}
```

Streamlit then renders the result using cards, tables, or metrics.

---

# 🎛️ Running the App

Start the app through Docker Compose:

```bash
docker compose up app
```

OR run the entire system:

```bash
docker compose up --build
```

Then visit:

```
http://localhost:8501
```

The app will automatically connect to the API and database.

---

# 🧩 Technologies Used

- **Streamlit** (UI framework)
- **Python (Pandas/Numpy)** for client-side processing
- **Requests** for API communication
- **FastAPI** for backend logic
- **PostgreSQL** as data source

---

# 🎉 Summary

The Streamlit application serves as the interactive layer of the system, enabling users to:

- Analyze sales data  
- Discover meaningful product bundles  
- Create campaigns using data-driven insights  
- Target specific customer segments  

It transforms backend analytics into an intuitive interface suitable for real-world marketing teams.

