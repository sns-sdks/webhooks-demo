"""
    Webhook for twitter.
"""
import base64
import hashlib
import hmac

from fastapi import APIRouter, Header, Request, Response

import config

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
        digestmod=hashlib.sha256
    ).digest()

    return {
        "response_token": f"sha256={base64.b64encode(sha256_hash_digest).decode()}"
    }


@tw_router.post("twitter")
async def webhook_event(signature: Header(None, alias="x-twitter-webhooks-signature"), request: Request):
    if config.SECURITY_CHECK:
        verify_request(signature=signature, body=request.body)
    return Response("")


def verify_request(signature, body):
    """
    :param signature:
    :param body:
    :return:
    """
    try:
        crc = base64.b64decode(signature[7:])  # strip out the first 7 characters
        h = hmac.new(
            key=bytes(config.TWITTER_CONSUMER_SECRET, 'ascii'),
            msg=body,
            digestmod=hashlib.sha256
        )
        return hmac.compare_digest(h.digest(), crc)
    except Exception as err:
        print(f"Exception in verify request: {err}")
        return False
