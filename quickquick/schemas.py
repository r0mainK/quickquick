"""Pydantic schemas used for responses."""

from pydantic import AnyHttpUrl, BaseModel


class UrlBody(BaseModel):
    original_url: AnyHttpUrl


class UrlResponse(BaseModel):
    id: str
    original_url: str
    nb_redirects: int
