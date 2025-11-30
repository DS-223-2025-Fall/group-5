"""
Database configuration for the ETL subsystem.

This module:
- Loads `DATABASE_URL` from the `.env` file.
- Creates a SQLAlchemy engine for ETL scripts.
- Exposes `SessionLocal` for transactional work.
- Provides `Base` for ORM models defined in `models.py`.
"""

import os

import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative
from dotenv import load_dotenv

# Load environment variables from .env placed at project root.
load_dotenv(".env")

# Connection string used by all ETL scripts.
DATABASE_URL = os.getenv("DATABASE_URL")

engine = sql.create_engine(DATABASE_URL)

# Session factory for ETL jobs that need explicit DB sessions.
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for ORM models.
Base = declarative.declarative_base()


def get_db():
    """
    Yield a database session for ETL scripts.

    Usage:
        with next(get_db()) as db:
            ...

    The session is closed automatically when the generator exits.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
