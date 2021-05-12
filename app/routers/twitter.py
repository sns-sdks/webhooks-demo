"""
    Webhook for twitter.
"""
import base64
import hashlib
import hmac
from typing import Optional

from fastapi import APIRouter, Header, Query, Request, Response

import config
from app.entities.twitter import Payload, RegisterWebhookItem
from app.deps import tw_cli

tw_router = APIRouter()

TWITTER_BASE_URL = "https://api.twitter.com/1.1/account_activity"


@tw_router.get("/twitter")
async def verify_challenge(crc_token: str):
    """
    Verify challenge for twitter
    """
    sha256_hash_digest = hmac.new(
        key=config.TWITTER_CONSUMER_SECRET.encode(),
        msg=crc_token.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    return {"response_token": f"sha256={base64.b64encode(sha256_hash_digest).decode()}"}


@tw_router.post("/twitter")
async def webhook_event(
    data: Payload,
    request: Request,
    signature: Optional[str] = Header(None, alias="x-twitter-webhooks-signature"),
):
    """
    Receive webhook push events, More see
    https://developer.twitter.com/en/docs/twitter-api/enterprise/account-activity-api/guides/account-activity-data-objects
    """
    if config.SECURITY_CHECK:
        vst = await verify_request(signature=signature, body=request.body)
        print(f"Verify status: {vst}")
    print(f"Event data:\n{data.dict()}")
    return Response("")


async def verify_request(signature: str, body):
    """
    :param signature: signature in headers
    :param body: body for request
    :return: bool
    """
    try:
        crc = base64.b64decode(signature[7:])  # strip out the first 7 characters
        h = hmac.new(
            key=bytes(config.TWITTER_CONSUMER_SECRET, "ascii"),
            msg=body,
            digestmod=hashlib.sha256,
        )
        return hmac.compare_digest(h.digest(), crc)
    except Exception as err:
        print(f"Exception in verify request: {err}")
        return False


# Manage Webhooks
@tw_router.get("/twitter/hooks")
async def list_webhooks(response: Response):
    """
    Returns all webhooks for app
    """
    resp = await tw_cli.get(url=f"{TWITTER_BASE_URL}/all/webhooks.json")
    response.status_code = resp.status_code
    return resp.json()


@tw_router.get("/twitter/hook/challenge")
async def trigger_challenge(
    env: str = Query(..., description="dev environment name"),
    webhook_id: str = Query(..., description="ID for webhook"),
    response: Response = None,
):
    """
    Manually trigger a CRC request.
    """
    resp = await tw_cli.put(
        url=f"{TWITTER_BASE_URL}/all/{env}/webhooks/{webhook_id}.json"
    )
    response.status_code = resp.status_code
    return {}


@tw_router.post("/twitter/hook/register")
async def register_webhook(body: RegisterWebhookItem, response: Response):
    """
    Register new webhook
    """
    resp = await tw_cli.post(
        url=f"{TWITTER_BASE_URL}/all/{body.env}/webhooks.json",
        params={"url": body.url},
    )
    response.status_code = resp.status_code
    return resp.json()


@tw_router.delete("/twitter/webhook")
async def delete_webhook(
    env: str = Query(..., description="dev environment name"),
    webhook_id: str = Query(..., description="ID for webhook"),
    response: Response = None,
):
    """
    Delete a webhook
    """
    resp = await tw_cli.delete(
        url=f"{TWITTER_BASE_URL}/all/{env}/webhooks/{webhook_id}.json"
    )
    response.status_code = resp.status_code
    return {}
