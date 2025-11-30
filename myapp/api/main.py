"""
Smart Packaging Optimizer – FastAPI Backend

Responsibilities:
-----------------
- Initialize FastAPI app.
- Create PostgreSQL tables at startup.
- Provide root & health-check endpoints.
- Include all API routes from routes.py.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from routes import router as api_router
from Database import models
from Database.database import engine, get_db

# Create all tables (dev/demo mode)
models.Base.metadata.create_all(bind=engine)

# Initialize API
app = FastAPI(
    title="Smart Packaging Optimizer API",
    description="Backend service for product analytics, customer insights, and bundle rule recommendations.",
    version="1.0.0",
)


# ---------------------------------------------------
# ROOT & HEALTH
# ---------------------------------------------------
@app.get("/")
def root():
    """
    Simple welcome endpoint to verify that the API is running.
    """
    return {"message": "Backend is connected to PostgreSQL 🎉"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Verify DB connection + API health.
    Returns "ok" if the database is reachable.
    """
    db.execute("SELECT 1")
    return {"status": "ok"}


# Include all versioned API endpoints under /api/...
app.include_router(api_router)
