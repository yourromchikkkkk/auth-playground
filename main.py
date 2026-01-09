from fastapi import FastAPI
from modules.healthcheck.router import healthcheck_router

app = FastAPI(
    title="Auth Playground",
    description="FastAPI auth playground",
    version="1.0.0"
)

app.include_router(healthcheck_router, tags=["healthcheck"])

@app.get("/")
async def root():
    return {"message": "Welcome to Auth Playground API"}

