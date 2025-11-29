"""
Core SQLAlchemy database configuration for the Marketing Analytics app.

Responsibilities
----------------
- Load the DATABASE_URL from the environment (works both locally and in Docker).
- Create the SQLAlchemy engine.
- Expose `SessionLocal`, a session factory used across the app.
- Define the declarative `Base` class for ORM models.
- Provide `get_db()` generator used as a dependency in FastAPI routes.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env so DATABASE_URL is available both locally and in Docker
load_dotenv()

# Connection string for the main application database.
# Example (Postgres):
#   postgresql+psycopg2://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Failing fast here makes configuration issues obvious during startup.
    raise ValueError("DATABASE_URL environment variable is not set")

# `pool_pre_ping=True` prevents stale connections in long-running services.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Session factory used by the API layer.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models (see models.py).
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session.

    Usage:
        def some_route(db: Session = Depends(get_db)):
            ...

    The session is:
    - created at the beginning of the request,
    - yielded to the route handler,
    - automatically closed when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
