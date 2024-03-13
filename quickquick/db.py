"""Database creation."""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_FILEPATH = os.environ.get("SQLITE_FILEPATH", "./sqlite.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_FILEPATH}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
