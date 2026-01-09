"""
Database base configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# TODO: update this with ENV variable
DATABASE_URL = "sqlite:///./data/app.db"

# Create engine
if "sqlite" in DATABASE_URL:
    db_path = DATABASE_URL.replace("sqlite:///", "")
    # Handle relative paths
    if db_path.startswith("./"):
        db_path = db_path[2:]
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

Base = declarative_base()

