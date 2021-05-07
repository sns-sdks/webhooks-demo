"""
    Webhook for facebook.
"""

from fastapi import APIRouter, Query, Response

import config
from app.entities.facebook import Payload

fb_router = APIRouter()


@fb_router.get("/facebook")
async def verify_challenge(
    mode: str = Query(None, alias="hub.mode"),
    verify_token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge"),
):
    """
    :return:
    """
    if not (mode and verify_token and challenge):
        return Response("hello")

    if verify_token == config.FACEBOOK_VERIFY_TOKEN and mode == "subscribe":
        return Response(challenge)
    return Response("hello")


@fb_router.post("/facebook")
async def webhook_event(data: Payload):
    print(f"Event data:\n{data.dict()}")
    return Response("ok")
