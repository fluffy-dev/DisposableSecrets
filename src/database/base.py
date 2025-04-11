"""Base module for SQLAlchemy declarative models."""
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Naming convention for PostgreSQL indexes and constraints
POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models with metadata and naming convention."""
    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)