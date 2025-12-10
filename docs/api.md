# API Service (FastAPI)

The API is the backend of the Beauty Bundling Recommendation System.  
It provides access to the PostgreSQL database, performs bundle recommendation computations, and exposes endpoints used by the Streamlit application.

The API is implemented using **FastAPI**, chosen for its speed, automatic documentation, and strong integration with Pydantic models.

---

# ⚙️ Purpose of the API

The API enables:

- Access to products, customers, and transaction data  
- Computation of product bundles using association rule mining  
- Serving bundle recommendations to Streamlit  
- Creating marketing campaigns  
- Decoupling backend logic from the frontend UI  

All responses are validated using **Pydantic models**.

---
# 📁 API Folder Structure

The FastAPI service is located in the `myapp/api/` directory.  
Below is the accurate structure based on the current project:

```
myapp/
└── api/
    ├── __init__.py
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── routes/
    │   ├── __init__.py
    │   └── ... (route definitions: products, bundles, campaigns)
    ├── crud/
    │   ├── __init__.py
    │   └── ... (database queries, bundle logic)
    └── Database/
        ├── __init__.py
        ├── database.py      # SQLAlchemy engine + session
        ├── db_helpers.py    # Utility functions (optional)
        ├── models.py        # Pydantic or ORM models
        └── schema.py        # Table schemas / validators
```

### 📌 Folder Descriptions

- **main.py**  
  Entry point of the FastAPI app. Includes startup events & router registration.

- **routes/**  
  Contains individual API endpoints grouped by feature (products, bundles, campaigns).

- **crud/**  
  Database access logic: queries, inserts, updates.  
  Bundle generation logic may also reside here.

- **Database/**  
  Contains the database layer:  
  - `database.py` – connection + session  
  - `models.py` – ORM models  
  - `schema.py` – Pydantic schemas  
  - `db_helpers.py` – helpers or utilities  

- **Dockerfile**  
  Builds the FastAPI service container.

- **requirements.txt**  
  Lists Python dependencies for the API.


---

# 🚀 Running the API

Run using Docker:

```bash
docker compose up api
```

Or run manually (if the environment is set up):

```bash
uvicorn api.main:app --reload
```

When running, visit:

🔗 **Interactive API docs (Swagger UI):**  
```
http://localhost:8000/docs
```

---

# 🔌 API Endpoints

All endpoints are mounted under the `/api` prefix (see `router = APIRouter(prefix="/api")`).

---

## 🧴 Products

### `GET /api/products/`
**Description:**  
Return the full list of products in the catalog.

**Query parameters:**  
- *(none)*

**Response:**  
`200 OK` – `list[Product]`  
Each product includes fields such as SKU, name, category, brand and price (see `Database.schema.Product`).

---

### `POST /api/products/`
**Description:**  
Create a new product in the catalog.

**Request body:**  
`ProductCreate` – new product details (name, category, brand, price, etc.)

**Response:**  
`201 Created` – `Product`  
The newly created product, including its generated ID/SKU.

---

## 👥 Customers

### `GET /api/customers/`
**Description:**  
Return all customers in the database.

**Query parameters:**  
- *(none)*

**Response:**  
`200 OK` – `list[Customer]`  
Each record corresponds to `Database.schema.Customer` (e.g. id, name, contact info, segment flags).

---

### `POST /api/customers/`
**Description:**  
Create a new customer.

**Request body:**  
`CustomerCreate` – fields for a new customer (name, email, etc.)

**Response:**  
`201 Created` – `Customer`  
The created customer with its database ID.

---

## 🗓 Timeframe (Date Dimension)

### `GET /api/timeframe/`
**Description:**  
Return all timeframe rows (date dimension table).

**Query parameters:**  
- *(none)*

**Response:**  
`200 OK` – `list[Timeframe]`  
Rows typically include date, day, month, year and other derived fields.

---

### `POST /api/timeframe/`
**Description:**  
Insert a new row into the timeframe table.

**Request body:**  
`TimeframeCreate` – fields describing a date (date, day, month, year, etc.)

**Response:**  
`201 Created` – `Timeframe`  
The inserted row.

---

## 🧾 Transactions (Order Headers)

### `GET /api/transactions/`
**Description:**  
Return all transactions (order headers).

**Query parameters:**  
- *(none)*

**Response:**  
`200 OK` – `list[Transaction]`  
Each transaction usually contains customer_id, time_id, total amount, channel, payment type, etc.

---

### `POST /api/transactions/`
**Description:**  
Create a new transaction (order header).

**Request body:**  
`TransactionCreate` – customer id, time id, total amount and other metadata.

**Response:**  
`201 Created` – `Transaction`  
The created transaction.

---

## 🧾 Sales (Line Items)

### `GET /api/sales/`
**Description:**  
Return all sales line items.

**Query parameters:**  
- *(none)*

**Response:**  
`200 OK` – `list[Sale]`  
Each sale connects a transaction to a product with quantity and pricing.

---

### `POST /api/sales/`
**Description:**  
Create a new sale (line item) tied to a transaction and product.

**Request body:**  
`SaleCreate` – transaction_id, product_sku, quantity, unit_price, etc.

**Response:**  
`201 Created` – `Sale`  
The created sale record.

---

## 📊 Analytics

### `GET /api/analytics/top-products/`
**Description:**  
Return the **top-N products ranked by revenue**.

**Query parameters:**
- `limit` *(int, optional, default = 10)* – number of products to return.

**Response:**  
`200 OK` – `list[TopProduct]`  
Each record includes product identification plus aggregated metrics (e.g. total revenue).

This endpoint is used by the dashboard to populate “Top Products” charts.

---

## 🧠 Bundle Rules

### `GET /api/rules/`
**Description:**  
Return **pre-computed bundle rules**, sorted by lift (strongest associations first).  
These rules typically come from association-rule mining over historical transactions (and may be seeded from `baseline_rules.xlsx`).

**Query parameters:**
- `limit` *(int, optional, default = 10)* – maximum number of rules to return.

**Response:**  
`200 OK` – `list[BundleRuleOut]`  

Each rule includes:

- the products in the bundle  
- metrics such as support, confidence, lift  
- possibly extra fields (e.g. popularity / score), depending on `Database.schema.BundleRuleOut`.

These rules power the bundle recommendation section in the UI.

---

# 📊 Internal Logic (Behind the Endpoints)

### 1. **Products Retrieval**
Uses simple SQLAlchemy queries:

```python
db.query(Product).all()
```

### 2. **Bundle Generation**
The API computes:

- Item frequencies  
- Co-occurrences  
- Conditional probabilities  
- Lift metrics  

and applies user-chosen thresholds.

The computation is optimized to run fast on 2,500+ transactions.

### 3. **Campaigns**
Currently stored in a simple DB table, simulating:

- Campaign creation  
- Storage  
- Summary generation  

---

# 🔒 Error Handling

The API validates:

- Threshold inputs  
- Non-existing products  
- Invalid campaign structures  
- Division by zero in lift calculations  

Errors return FastAPI-standard JSON responses.

---

# 📚 API Documentation via Swagger

FastAPI automatically generates docs:

```
http://localhost:8008/docs
```

and Redoc:

```
http://localhost:8008/redoc
```

These pages show:

- All endpoints  
- Example requests  
- Example responses  
- Schema definitions  

Useful for debugging and development.

---

# 🧩 API in the System Architecture

```
Streamlit → FastAPI → PostgreSQL → ML Bundle Engine
```

The API is the bridge between raw data and the user interface.

It ensures:

- Data integrity  
- Fast computation  
- Standardized communication  
- Easy integration with UI or external tools  

---

# 🎉 Summary

The FastAPI backend powers the intelligence of the system:

- Serves product & transaction data  
- Computes bundle recommendations  
- Validates ML results using Pydantic models  
- Supports campaign creation  
- Connects the UI, database, and ML logic  

It is designed to be modular, scalable, and easily extendable.

