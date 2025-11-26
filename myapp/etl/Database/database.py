import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative
from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = sql.create_engine(DATABASE_URL)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
