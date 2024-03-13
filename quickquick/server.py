"""FastAPI server."""

import os

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="URL shortener",
    openapi_url=None
    if os.environ.get("DISABLE_DOCUMENTATION") == "true"
    else "/openapi.json",
)


def _get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _register_redirect(url_id: str):
    """Register a redirection."""
    with SessionLocal() as db:
        crud.increment_redirect_count(db, url_id)


@app.get("/url/", response_model=schemas.UrlResponse)
def read_url(url_id: str, db: Session = Depends(_get_db)):
    """Retrieve the original URL and redirect count from its ID."""
    db_url = crud.get_url_from_id(db, url_id)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not yet registered")
    return db_url


@app.post("/url/", response_model=schemas.UrlResponse)
def short_url(body: schemas.UrlBody, db: Session = Depends(_get_db)):
    """Create short URL."""
    db_url = crud.get_url_from_original_url(db, str(body.original_url))
    if db_url is None:
        db_url = crud.create_url(db, str(body.original_url))
    return db_url


@app.get("/{url_id}", status_code=302, response_class=RedirectResponse)
def redirect_url(
    url_id: str, background_tasks: BackgroundTasks, db: Session = Depends(_get_db)
):
    """Redirect a short URL by mapping to the original one."""
    db_url = crud.get_url_from_id(db, url_id)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not yet registered")
    background_tasks.add_task(_register_redirect, url_id)
    return db_url.original_url


@app.get("/", status_code=308, response_class=RedirectResponse)
def redirect_homepage():
    """Redirect the homepage to the static path to avoid collision."""
    return "/static/index.html"


app.mount(
    "/static", StaticFiles(directory="quickquick/static", html=True), name="static"
)
