"""
Database base configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

Base = declarative_base()

_engine = None
_SessionLocal = None

def _init_db():
    """Initialize database engine and session (called lazily to avoid circular imports)"""
    global _engine, _SessionLocal
    if _engine is None:
        from modules.core import settings
        
        # Create engine
        database_url = str(settings.DATABASE_URL)
        if "sqlite" in database_url:
            db_path = database_url.replace("sqlite:///", "")
            # Handle relative paths
            if db_path.startswith("./"):
                db_path = db_path[2:]
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
        
        _engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
        )
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine, _SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    _, SessionLocal = _init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class _EngineProxy:
    """Proxy for engine that initializes lazily"""
    def __getattr__(self, name):
        db_engine, _ = _init_db()
        return getattr(db_engine, name)
    
    def __repr__(self):
        db_engine, _ = _init_db()
        return repr(db_engine)

engine = _EngineProxy()
