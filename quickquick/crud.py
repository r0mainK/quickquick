"""CRUD operations."""

import hashlib

from sqlalchemy.orm import Session

from . import models


def get_url_from_id(db: Session, url_id: str) -> models.Urls | None:
    """Get an URL object from its id."""
    return db.query(models.Urls).filter(models.Urls.id == url_id).first()


def get_url_from_original_url(db: Session, original_url: str) -> models.Urls | None:
    """Get an URL object from its orignal url."""
    return (
        db.query(models.Urls).filter(models.Urls.original_url == original_url).first()
    )


def create_url(db: Session, original_url: str, length: int = 10) -> models.Urls:
    """Create an URL object by hashing the original URL."""
    url_id = hashlib.shake_256(original_url.encode()).hexdigest(length // 2)
    db_url = models.Urls(id=url_id, original_url=original_url, nb_redirects=0)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def increment_redirect_count(db: Session, url_id: str):
    """Increment the redirection count of an URL object."""
    db_url = get_url_from_id(db, url_id)
    db_url.nb_redirects += 1
    db.commit()
    db.refresh(db_url)
