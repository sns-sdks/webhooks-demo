"""
    Tests for twitter webhook.
"""

import pytest
import respx
from httpx import AsyncClient, Response

from app.main import app


@pytest.mark.asyncio
async def test_verify_challenge():
    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.get("/twitter", params={"crc_token": "token"})
        assert resp.status_code == 200
        assert (
                resp.json()["response_token"]
                == "sha256=5LjCS431VjMzel8lfVzi3wz95Am3liDPzmmJdboAU0s="
        )


@pytest.mark.asyncio
async def test_webhook_event():
    tweet_delete_events = {
        "for_user_id": "930524282358325248",
        "tweet_delete_events": [
            {
                "status": {
                    "id": "1045405559317569537",
                    "user_id": "930524282358325248",
                },
                "timestamp_ms": "1432228155593",
            }
        ],
    }
    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.post("/twitter", json=tweet_delete_events)
        assert resp.status_code == 200
        assert resp.text == ""


@respx.mock
@pytest.mark.asyncio
async def test_list_webhooks():
    resp_data = [
        {
            "id": "1234567890",
            "url": "https://your_domain.com/webhook/twitter/0",
            "valid": True,
            "created_at": "2016-06-02T23:54:02Z",
        }
    ]
    respx.get("https://api.twitter.com/1.1/account_activity/all/webhooks.json").mock(
        return_value=Response(status_code=200, json=resp_data)
    )

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.get("/twitter/hooks")
        assert resp.status_code == 200
        assert resp.json()[0]["id"] == "1234567890"


@respx.mock
@pytest.mark.asyncio
async def test_trigger_challenge():
    params = {"env": "env", "webhook_id": 1}

    respx.put("https://api.twitter.com/1.1/account_activity/all/env/webhooks/1.json").mock(
        return_value=Response(status_code=204)
    )

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.get("/twitter/hook/challenge", params=params)
        assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_register_webhook():
    body = {"env": "env", "url": "https://example.com/webhook/twitter"}

    webhook_data = {
        "id": "1234567890",
        "url": "https://example.com/webhook/twitter",
        "valid": True,
        "created_at": "2016-06-02T23:54:02Z"
    }

    respx.post("https://api.twitter.com/1.1/account_activity/all/env/webhooks.json").mock(
        return_value=Response(status_code=200, json=webhook_data)
    )

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.post("/twitter/hook/register", json=body)
        assert resp.status_code == 200
        assert resp.json()["id"] == "1234567890"


@respx.mock
@pytest.mark.asyncio
async def test_delete_webhook():
    params = {"env": "env", "webhook_id": 1}

    respx.delete("https://api.twitter.com/1.1/account_activity/all/env/webhooks/1.json").mock(
        return_value=Response(status_code=204)
    )

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.delete("/twitter/webhook", params=params)
        assert resp.status_code == 204
