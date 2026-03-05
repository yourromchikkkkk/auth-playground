from fastapi import FastAPI

from app.database.base import Base, _init_db, get_session
from app.scripts import generate_asymmetric_keys, populate_user_into_db, create_super_admin_user
import os
from app.modules.core import settings

# routers
from app.modules.healthcheck.router import healthcheck_router
from app.modules.user.router import user_router

# database models
from app.modules import User, Role

app = FastAPI(
    title=f"Auth Playground v.{settings.SERVICE_VERSION}",
    description="FastAPI auth playground",
    version=settings.SERVICE_VERSION
)

@app.on_event("startup")
async def startup_event():
    """Create tables and seed initial data"""
    db_engine, _ = _init_db()
    try:
        Base.metadata.create_all(bind=db_engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise e

    db = get_session()
    try:
        populate_user_into_db(db)
        create_super_admin_user(db)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
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
