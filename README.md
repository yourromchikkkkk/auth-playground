# Auth Playground

A FastAPI project with modular architecture where each module contains its own models, controllers, routers, and validation schemas.

## Project Structure

```
auth-playground/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── database/              # Database configuration
│   ├── __init__.py
│   └── base.py           # Database base, engine, session
├── modules/               # Application modules
│   ├── __init__.py
│   └── healthcheck/       # Healthcheck module
│       ├── __init__.py
│       ├── models.py      # Domain models (business logic)
│       ├── db_models.py   # Database/ORM models (SQLAlchemy)
│       ├── schemas.py     # Pydantic validation schemas
│       ├── controller.py  # Business logic
│       └── router.py      # API routes
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

- **`database/`**: Central database configuration
  - `base.py`: Database engine, session factory, and base model class
  - All modules import from here: `from database.base import Base, get_db`

- **`modules/{module_name}/db_models.py`**: Module-specific database models
  - Each module defines its own SQLAlchemy models
  - All models inherit from `database.base.Base`
  - Keeps database models scoped to their respective modules

### Example Database Model Structure

```python
# modules/users/db_models.py
from sqlalchemy import Column, Integer, String
from database.base import Base

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
from database.base import get_db

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

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/healthcheck` - Check the health status of the service

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Adding New Modules

To add a new module:

1. Create a new directory under `modules/` (e.g., `modules/users/`)
2. Create the following files:
   - `__init__.py`
   - `models.py` - Domain models (business logic)
   - `db_models.py` - Database/ORM models (if needed)
   - `schemas.py` - Pydantic validation schemas
   - `controller.py` - Business logic
   - `router.py` - API routes
3. Register the router in `main.py`:
```python
from modules.users.router import users_router
app.include_router(users_router, tags=["users"])
```

### Database Setup

1. Update `database/base.py` with your database connection string
2. Create database tables (using Alembic migrations recommended):
```python
from database.base import Base, engine
from modules.users.db_models import User  # Import all models
# ... import other module models

Base.metadata.create_all(bind=engine)
```

