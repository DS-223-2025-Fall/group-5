# API – Clustr Backend

The Clustr backend is implemented with FastAPI and exposes REST endpoints for accessing master data, transactional data, association rules, and ML-based bundle recommendations.

Base URL in local development:

    http://127.0.0.1:8008

Interactive API docs (Swagger UI):

    http://127.0.0.1:8008/docs

---

## 1. Base Endpoints

### GET /

Returns a simple JSON payload confirming that the service is running.

Example response:

    {
      "service": "Clustr API",
      "status": "ok"
    }

---

### GET /health

Checks that the API and database are reachable.

Example response:

    {
      "status": "ok"
    }

---

## 2. Product Endpoints

These endpoints work with the `products` table and corresponding Pydantic schemas.

### GET /api/products/

Returns all products.

Fields:

- product_sku  
- product_name  
- category  
- brand  
- price  

---

### POST /api/products/

Creates a new product.

Request body (conceptual structure):

- product_name  
- category  
- brand  
- price  

Example request:

    {
      "product_name": "Moisturizer X",
      "category": "Skincare",
      "brand": "FreshLine",
      "price": 19.99
    }

Response:

- Returns the created product, including its `product_sku`.

---

## 3. Customer Endpoints

These endpoints work with the `customers` table.

### GET /api/customers/

Returns all customers.

Fields:

- customer_id  
- first_name  
- last_name  
- gender  
- age  
- dob  
- email  
- phone  
- city  
- income_level  
- shopping_preference  
- customer_segment  

---

### POST /api/customers/

Creates a new customer.

Request body (conceptual structure):

- first_name  
- last_name  
- gender  
- age  
- dob  
- email  
- phone  
- city  
- income_level  
- shopping_preference  
- customer_segment  

Response:

- Returns the created customer, including `customer_id`.

---

## 4. Timeframe Endpoints

The `timeframe` table stores calendar information for analytics.

### GET /api/timeframe/

Returns all timeframe rows.

Fields:

- time_id  
- date  
- day  
- month  
- year  

---

### POST /api/timeframe/

Creates a new timeframe record.

Request body (conceptual structure):

- date  
- day  
- month  
- year  

Response:

- Returns the created timeframe entry.

---

## 5. Transaction Endpoints

Transactions represent a completed purchase made by a customer at a specific time.

### GET /api/transactions/

Returns all transactions.

Fields:

- transaction_id  
- customer_id  
- time_id  
- transaction_amount  
- channel  
- payment_type  

---

### POST /api/transactions/

Creates a new transaction.

Request body (conceptual structure):

- customer_id  
- time_id  
- transaction_amount  
- channel  
- payment_type  

Response:

- Returns the created transaction, including `transaction_id`.

---

## 6. Sales Endpoints

Sales are line items within a transaction, each referring to a specific product.

### GET /api/sales/

Returns all sales line items.

Fields:

- sale_id  
- transaction_id  
- product_sku  
- quantity  
- unit_price  
- line_total  

---

### POST /api/sales/

Creates a new sales line item.

Request body (conceptual structure):

- transaction_id  
- product_sku  
- quantity  
- unit_price  

Response:

- Returns the created sale, including `sale_id` and computed `line_total` where applicable.

---
