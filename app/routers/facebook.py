"""
    Webhook for facebook.
"""

from fastapi import APIRouter, Body, Query, Response

import config
from app.entities.facebook import Payload, SubscribeForm
from app.deps import fb_cli

router = APIRouter()
FACEBOOK_GRAPH_URL = "https://graph.facebook.com"


@router.get("/facebook")
async def verify_challenge(
    mode: str = Query(
        ..., alias="hub.mode", description="Mode is always be `subscribe`"
    ),
    verify_token: str = Query(
        ...,
        alias="hub.verify_token",
        description="Token which you set at app dashboard",
    ),
    challenge: str = Query(
        ..., alias="hub.challenge", description="A random string return to facebook"
    ),
):
    """
    Verify challenge for webhook.
    """
    if not (mode and verify_token and challenge):
        return Response("hello")

    if verify_token == config.FACEBOOK_VERIFY_TOKEN and mode == "subscribe":
        return Response(challenge)
    return Response("hello")


@router.post("/facebook")
async def webhook_event(
    data: Payload = Body(..., description="Json data from facebook")
):
    """
    Receive webhook push events, More see
    https://developers.facebook.com/docs/graph-api/webhooks/getting-started#event-notifications
    """
    print(f"Event data:\n{data.dict()}")
    return Response("ok")


@router.post("/facebook/subscribed_apps")
async def subscribe_webhook(body: SubscribeForm, response: Response):
    """
    Subscribe your page to webhook
    """
    resp = await fb_cli.post(
        url=f"{FACEBOOK_GRAPH_URL}/{body.page_id}/subscribed_apps",
        params={
            "subscribed_fields": body.subscribe_fields,
            "access_token": body.access_token,
        },
    )
    response.status_code = resp.status_code
    return resp.json()


@router.delete("/facebook/subscribed_apps")
async def delete_subscribe_webhook(
    page_id: str = Query(..., description="ID for facebook page"),
    access_token: str = Query(..., description="page access token"),
    response: Response = None,
):
    """
    Remove page from webhook subscription
    """
    resp = await fb_cli.delete(
        url=f"{FACEBOOK_GRAPH_URL}/{page_id}/subscribed_apps",
        params={"access_token": access_token},
    )
    response.status_code = resp.status_code
    return resp.json()


@router.get("/facebook/subscribed_apps")
async def list_page_subscribed_apps(
    page_id: str = Query(..., description="ID for facebook page"),
    access_token: str = Query(..., description="page access token"),
    response: Response = None,
):
    """
    list page have subscribed apps
    """
    resp = await fb_cli.get(
        url=f"{FACEBOOK_GRAPH_URL}/{page_id}/subscribed_apps",
        params={"access_token": access_token},
    )
    response.status_code = resp.status_code
    return resp.json()
