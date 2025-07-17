"""
Database configuration and connection management
"""

import os
import asyncpg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from .settings import settings

# SQLAlchemy setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def get_db_connection():
    """Get async database connection for asyncpg"""
    return await asyncpg.connect(settings.DATABASE_URL)

def get_db():
    """Get database session for SQLAlchemy"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)