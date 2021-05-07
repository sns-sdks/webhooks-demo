"""
    Data model for facebook
"""
from typing import List

from pydantic import BaseModel


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
