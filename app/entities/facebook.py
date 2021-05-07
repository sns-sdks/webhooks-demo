"""
    Data model for facebook
"""
from typing import List

from pydantic import BaseModel, Field


class ChallengeForm(BaseModel):
    hub_mode: str = Field(None, alias="hub.mode")
    hub_verify_token: str = Field(None, alias="hub.verify_token")
    hub_challenge: str = Field(None, alias="hub.challenge")


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
