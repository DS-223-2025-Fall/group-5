# Clustr Application (Streamlit UI)

The Clustr Streamlit application is the main user-facing interface for analysts and marketers.  
It provides dashboards, database exploration tools, segmentation filters, and product bundle recommendations powered by both association rules and machine learning.

All application-related code is stored in the `app/` directory.

---

## 1. Application Structure

The Streamlit application is organized into multiple modular pages:

- **Login** – authentication and session initialization  
- **Dashboard** – high-level KPIs, visual analytics, and customer insights  
- **Database** – exploration of PostgreSQL tables  
- **Bundles** – association-rule and ML-based bundle discovery  
- **Campaigns** – create campaign concepts based on selected bundles  
- **Settings** – configure user and application preferences  

---

## 2. Login Page

The login page provides simple session-based access control.

Features:

- username and password fields  
- basic validation  
- session state management  

After logging in, users can navigate freely across all app sections.

---

## 3. Dashboard Page

The dashboard provides visual summaries of the synthetic retail dataset loaded by the ETL pipeline.

Typical insights displayed:

- total sales and revenue trends  
- top-performing products  
- customer demographics (age, gender, income level)  
- category and brand-level breakdowns  
- daily / monthly / yearly performance charts  

This page helps orient analysts and provides a data-driven overview.

---

## 4. Database Explorer

The Database page connects directly to PostgreSQL and allows users to inspect data tables.

Capabilities:

- selectable table dropdown  
- preview of rows  
- column metadata  
- dynamic table refresh  
- scrollable, paginated content  

It provides a simple way to validate ETL results or understand database structure.

---

## 5. Bundles Page

The Bundles page is the core analytical section of the Clustr application.

### Filters available:

- gender  
- age range  
- income level  
- customer segment  
- shopping preference  

### Outputs displayed:

- association-rule bundles from the `bundle_rules` table  
- ML-recommended bundles, ranked by predicted success score  

Each bundle includes:

- bundle items (antecedents + consequents)  
- support  
- confidence  
- lift  
- ML score (if using the prediction model)  

This page empowers marketers to identify high-value product combinations.

---

## 6. Campaigns Page

The Campaigns page helps convert insights into actionable ideas.

It allows the user to:

- select a recommended bundle  
- target a specific customer segment  
- generate messaging suggestions  
- outline promotional strategies  

This bridges analytics with practical marketing execution.

---

## 7. Settings Page

The Settings page supports configuration options for Clustr.

Possible settings:

- number of bundles to display  
- ML threshold sensitivity  
- UI configuration options  
- demo mode toggles  

These settings help customize the user experience.

---

## 8. API & Database Connectivity

The Streamlit application interacts with:

### FastAPI backend
Used for:

- fetching master and transactional data  
- retrieving association rules  
- fetching ML-based recommendations  

### PostgreSQL database
Used for:

- direct table inspection  
- validating ETL-loaded data  

This dual-access strategy ensures both operational reliability and debugging flexibility.

---

## 9. Running the App

To launch the Streamlit UI:

    streamlit run app/app.py

The application will be available at:

    http://localhost:8501

Users must log in before accessing other pages.

---

## 10. Role of the Streamlit App in the Clustr Ecosystem

The app serves as the primary interface for non-technical users.

It enables:

- intuitive data visualization  
- interactive segmentation filtering  
- real-time ML bundle recommendation exploration  
- campaign planning based on bundle insights  

Clustr’s architecture ensures that the Streamlit UI always reflects the latest ETL-loaded and API-exposed data.

---

## 11. Summary

The Clustr Streamlit application provides a complete analytical experience, allowing users to:

- explore generated retail datasets  
- visualize customer behavior  
- analyze product performance  
- discover high-value product bundles  
- plan marketing campaigns  

This interactive layer makes Clustr accessible, practical, and impactful for end-users.
