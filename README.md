# Auth Playground

A FastAPI project with modular architecture where each module contains its own models, controllers, routers, and validation schemas.

## Project Structure

```
auth-playground/
├── app/                    # Application code
│   ├── main.py             # FastAPI application entry point
│   ├── database/           # Database configuration
│   │   ├── __init__.py
│   │   └── base.py         # Database base, engine, session
│   ├── modules/            # Application modules
│   │   ├── core/           # Config, security
│   │   ├── healthcheck/
│   │   └── user/
│   ├── utils/              # Shared utilities
│   └── scripts/            # Scripts (e.g. key generation)
├── data/                   # Database files (at root, not in app)
├── keys/                   # RSA keys (at root, not in app)
├── requirements.txt
└── README.md
```

## Module Architecture

Each module follows a clean architecture pattern with:

- **models.py**: Domain models and business entities (pure Python classes)
- **db_models.py**: Database/ORM models (SQLAlchemy models) - module-specific database tables
- **schemas.py**: Pydantic schemas for request/response validation
- **controller.py**: Business logic and orchestration
- **router.py**: FastAPI route definitions

## Database Architecture

The project uses a hybrid database approach:

- **`app/database/`**: Central database configuration
  - `base.py`: Database engine, session factory, and base model class
  - All modules import from here: `from app.database.base import Base, get_db`

- **`app/modules/{module_name}/db_models.py`**: Module-specific database models
  - Each module defines its own SQLAlchemy models
  - All models inherit from `app.database.base.Base`
  - Keeps database models scoped to their respective modules

### Example Database Model Structure

```python
# app/modules/user/db_models.py
from sqlalchemy import Column, Integer, String
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
```

### Using Database in Routes

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.base import get_db

@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    # Use db session here
    return db.query(Item).all()
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application (from project root; `data/` and `keys/` stay at root):
```bash
uvicorn app.main:app --reload
```
Or: `python -m app.main`

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/healthcheck` - Check the health status of the service

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Adding New Modules

To add a new module:

1. Create a new directory under `app/modules/` (e.g., `app/modules/users/`)
2. Create the following files:
   - `__init__.py`
   - `models.py` - Domain models (business logic)
   - `db_models.py` - Database/ORM models (if needed)
   - `schemas.py` - Pydantic validation schemas
   - `controller.py` - Business logic
   - `router.py` - API routes
3. Register the router in `app/main.py`:
```python
from app.modules.users.router import users_router
app.include_router(users_router, tags=["users"])
```

### Database Setup

1. Update `app/modules/core/config.py` (e.g. `DATABASE_URL`) or use `.env`
2. Create database tables (using Alembic migrations recommended):
```python
from app.database.base import Base, engine
from app.modules.user.db_models import User  # Import all models
# ... import other module models

Base.metadata.create_all(bind=engine)
```

