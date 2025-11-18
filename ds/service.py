from fastapi import FastAPI
from db import get_top_rules, init_db, load_rules_from_csv

app = FastAPI()


@app.get("/")
def home():
    return {"message": "DS Baseline Model Service Running"}


@app.get("/rules")
def rules(limit: int = 10):
    df = get_top_rules(limit)
    return df.to_dict(orient="records")


# Initialize DB at startup
@app.on_event("startup")
def startup():
    init_db()
    load_rules_from_csv()

