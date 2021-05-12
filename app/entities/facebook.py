"""
    Data model for facebook
"""
from typing import List

from pydantic import BaseModel, Field


class Change(BaseModel):
    field: str
    value: dict = None


class PayloadEntry(BaseModel):
    id: str
    time: int
    changed_fields: List[str] = None
    changes: List[dict] = None


class Payload(BaseModel):
    object: str
    entry: List[PayloadEntry]


class SubscribeForm(BaseModel):
    page_id: str = Field(..., description="ID for facebook page")
    fields: str = Field(..., description="Fields you want to subscribe to")
    access_token: str = Field(..., description="Page access token")
