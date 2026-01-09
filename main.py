from fastapi import FastAPI
from modules.healthcheck.router import healthcheck_router
from database.base import Base, engine

app = FastAPI(
    title="Auth Playground",
    description="FastAPI auth playground",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Create all tables in the DB"""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise e

app.include_router(healthcheck_router, tags=["healthcheck"])

@app.get("/")
async def root():
    return {"message": "Welcome to Auth Playground API"}

