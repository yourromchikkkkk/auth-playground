from fastapi import FastAPI
from database.base import Base, engine
from scripts import generate_asymmetric_keys
import os
from modules.core import settings

# routers
from modules.healthcheck.router import healthcheck_router
from modules.user.router import user_router

# database models
from modules import User

app = FastAPI(
    title=f"Auth Playground v.{settings.SERVICE_VERSION}",
    description="FastAPI auth playground",
    version=settings.SERVICE_VERSION
)

@app.on_event("startup")
async def startup_event():
    """Create all tables in the DB"""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise e
    
    # Generate asymmetric keys
    if not os.path.exists(f"{settings.KEYS_PATH}/public.pem") or not os.path.exists(f"{settings.KEYS_PATH}/private.pem"):
        print("Generating asymmetric keys...")
        try:
            generate_asymmetric_keys(settings.KEYS_PATH)
        except Exception as e:
            print(f"Error generating asymmetric keys: {e}")
            raise e

app.include_router(healthcheck_router, tags=["healthcheck"])
app.include_router(user_router, tags=["users"])

@app.get("/")
async def root():
    return {"message": f"Welcome to Auth Playground v.{settings.SERVICE_VERSION} API"}

