"""
    Webhook for twitter.
"""
import base64
import hashlib
import hmac
from typing import Optional
from urllib.parse import quote_plus

from fastapi import APIRouter, Header, Request, Response

import config
from app.entities.twitter import Payload, RegisterWebhookItem
from app.deps import tw_cli

tw_router = APIRouter()


@tw_router.get("/twitter")
async def verify_challenge(crc_token: str):
    """
    :param crc_token:
    :return:
    """
    sha256_hash_digest = hmac.new(
        key=bytes(config.TWITTER_CONSUMER_SECRET, "utf-8"),
        msg=bytes(crc_token, "utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    return {"response_token": f"sha256={base64.b64encode(sha256_hash_digest).decode()}"}


@tw_router.post("/twitter")
async def webhook_event(
    data: Payload,
    request: Request,
    signature: Optional[str] = Header(None, alias="x-twitter-webhooks-signature"),
):
    if config.SECURITY_CHECK:
        vst = await verify_request(signature=signature, body=request.body)
        print(f"Verify status: {vst}")
    print(f"Event data:\n{data.dict()}")
    return Response("")


async def verify_request(signature, body):
    """
    :param signature:
    :param body:
    :return:
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
    :param response:
    :return:
    """
    resp = await tw_cli.get(
        url="https://api.twitter.com/1.1/account_activity/all/webhooks.json"
    )
    response.status_code = resp.status_code
    return resp.json()


@tw_router.get("/twitter/hook/challenge")
async def trigger_challenge(env: str, webhook_id: str, response: Response):
    """
    :param env: app env name
    :param webhook_id: ID for webhook.
    :param response: Response
    :return:
    """
    resp = await tw_cli.put(
        url=f"https://api.twitter.com/1.1/account_activity/all/{env}/webhooks/{webhook_id}.json"
    )
    response.status_code = resp.status_code
    return resp.json()


@tw_router.post("/twitter/hook/register")
async def register_webhook(body: RegisterWebhookItem, response: Response):
    """
    :param body:
    :param response:
    :return:
    """
    resp = await tw_cli.post(
        url=f"https://api.twitter.com/1.1/account_activity/all/{body.env}/webhooks.json",
        params={"url": quote_plus(body.url)},
    )
    response.status_code = resp.status_code
    return resp.json()


@tw_router.delete("/twitter/{env}/webhook/{webhook_id}")
async def delete_webhook(env: str, webhook_id: str, response: Response):
    """
    :param env:
    :param webhook_id:
    :param response:
    :return:
    """
    resp = await tw_cli.delete(
        url=f"https://api.twitter.com/1.1/account_activity/all/{env}/webhooks/{webhook_id}.json"
    )
    response.status_code = resp.status_code
    return resp.json()
