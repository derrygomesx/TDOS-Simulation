"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

database.py

SQLAlchemy database configuration.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from config.config import settings


# ==========================================================
# DATABASE ENGINE
# ==========================================================

engine = create_engine(

    settings.database_url,

    echo=False,

)


# ==========================================================
# SESSION FACTORY
# ==========================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,

)


# ==========================================================
# BASE CLASS
# ==========================================================

Base = declarative_base()


# ==========================================================
# DATABASE HELPERS
# ==========================================================

def initialize_database() -> None:
    """
    Creates all database tables.
    """

    Base.metadata.create_all(bind=engine)


def get_session():
    """
    Returns a database session.
    """

    return SessionLocal()