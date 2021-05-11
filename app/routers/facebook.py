"""
    Webhook for facebook.
"""

from fastapi import APIRouter, Query, Response

import config
from app.entities.facebook import Payload, SubscribeForm
from app.deps import fb_cli

fb_router = APIRouter()
FACEBOOK_GRAPH_URL = "https://graph.facebook.com"


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


@fb_router.post("/facebook/subscribed_apps")
async def subscribe_webhook(body: SubscribeForm, response: Response):
    """
    :param body:
        - page_id: id for your page
        - fields: fields to subscribe
        - access_token: your page access token
    :param response:
    :return:
    """
    resp = await fb_cli.post(
        url=f"{FACEBOOK_GRAPH_URL}/{body.page_id}/subscribed_apps",
        params={
            "subscribed_fields": body.fields,
            "access_token": body.access_token,
        },
    )
    response.status_code = resp.status_code
    return resp.json()


@fb_router.get("/facebook/subscribed_apps")
async def list_page_subscribed_apps(
    page_id: str, access_token: str, response: Response
):
    """
    :param page_id:
    :param access_token:
    :param response:
    :return:
    """
    resp = await fb_cli.get(
        url=f"{FACEBOOK_GRAPH_URL}/{page_id}/subscribed_apps",
        params={"access_token": access_token},
    )
    response.status_code = resp.status_code
    return resp.json()
