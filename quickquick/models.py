"""SQLAlchemy models for the SQLite database."""

from sqlalchemy import Column, Integer, String

from .db import Base


class Urls(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True)
    original_url = Column(String, unique=True, index=True)
    nb_redirects = Column(Integer)
