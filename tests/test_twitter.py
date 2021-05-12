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
    respx.get("https://api.twitter.com/1.1/account_activity/webhooks.json").mock(
        return_value=Response(status_code=200, json=resp_data)
    )

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.get("/twitter/hooks")
        assert resp.status_code == 200
        assert resp.json()[0]["id"] == "1234567890"
