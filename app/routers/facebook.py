"""
    Webhook for facebook.
"""

from fastapi import APIRouter, Response

import config
from app.entities.facebook import ChallengeForm, Payload

fb_router = APIRouter()


@fb_router.get("/facebook")
async def verify_challenge(form: ChallengeForm):
    """
    :return:
    """
    if not (form.hub_mode and form.hub_verify_token and form.hub_challenge):
        return Response("hello")

    if form.hub_verify_token == config.FACEBOOK_VERIFY_TOKEN and form.hub_mode == "subscribe":
        return Response(form.hub_challenge)
    return Response("hello")


@fb_router.post("/facebook")
async def webhook_event(data: Payload):
    print(f"Event data:\n{data.dict()}")
    return Response("ok")
