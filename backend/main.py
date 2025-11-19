from fastapi import FastAPI
from backend.routes import router
from backend.database import init_db

app = FastAPI(title="Backend API", version="1.0.0")
app.include_router(router)


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
