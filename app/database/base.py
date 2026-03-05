"""
Database base configuration
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()

_engine = None
_SessionLocal = None


def _init_db():
    """Initialize database engine and session (called lazily to avoid circular imports)"""
    global _engine, _SessionLocal
    if _engine is None:
        from app.modules.core import settings

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

            connect_args = {"check_same_thread": False, "timeout": 30}
        else:
            connect_args = {}

        _engine = create_engine(database_url, connect_args=connect_args)

        if "sqlite" in database_url:

            @event.listens_for(_engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA busy_timeout=30000")
                cursor.close()

        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine, _SessionLocal


def get_session() -> Session:
    """Get a new database session (for startup/scripts). Caller must close it."""
    _, SessionLocal = _init_db()
    return SessionLocal()


def get_db() -> Generator[Session, None, None]:
    """Get database session (generator for FastAPI Depends)"""
    db = get_session()
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
