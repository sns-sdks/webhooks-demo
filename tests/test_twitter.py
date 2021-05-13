"""
    Tests for twitter webhook.
"""

import pytest
import respx
from httpx import Response


@pytest.mark.asyncio
async def test_verify_challenge(client):
    async with client:
        resp: Response = await client.get(
            "/webhook/twitter", params={"crc_token": "token"}
        )
        assert resp.status_code == 200
        assert (
            resp.json()["response_token"]
            == "sha256=5LjCS431VjMzel8lfVzi3wz95Am3liDPzmmJdboAU0s="
        )


@pytest.mark.asyncio
async def test_webhook_event(client):
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
    async with client:
        resp: Response = await client.post("/webhook/twitter", json=tweet_delete_events)
        assert resp.status_code == 200
        assert resp.text == ""


@respx.mock
@pytest.mark.asyncio
async def test_list_webhooks(client):
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

    async with client:
        resp: Response = await client.get("/webhook/twitter/webhooks")
        assert resp.status_code == 200
        assert resp.json()[0]["id"] == "1234567890"


@respx.mock
@pytest.mark.asyncio
async def test_trigger_challenge(client):
    params = {"env": "env", "webhook_id": 1}

    respx.put(
        "https://api.twitter.com/1.1/account_activity/all/env/webhooks/1.json"
    ).mock(return_value=Response(status_code=204))

    async with client:
        resp: Response = await client.get(
            "/webhook/twitter/webhook/challenge", params=params
        )
        assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_register_webhook(client):
    body = {"env": "env", "url": "https://example.com/webhook/twitter"}

    webhook_data = {
        "id": "1234567890",
        "url": "https://example.com/webhook/twitter",
        "valid": True,
        "created_at": "2016-06-02T23:54:02Z",
    }

    respx.post(
        "https://api.twitter.com/1.1/account_activity/all/env/webhooks.json"
    ).mock(return_value=Response(status_code=200, json=webhook_data))

    async with client:
        resp: Response = await client.post("/webhook/twitter/webhook", json=body)
        assert resp.status_code == 200
        assert resp.json()["id"] == "1234567890"


@respx.mock
@pytest.mark.asyncio
async def test_delete_webhook(client):
    params = {"env": "env", "webhook_id": 1}

    respx.delete(
        "https://api.twitter.com/1.1/account_activity/all/env/webhooks/1.json"
    ).mock(return_value=Response(status_code=204))

    async with client:
        resp: Response = await client.delete("/webhook/twitter/webhook", params=params)
        assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_subscribe_webhook(client):
    body = {"env": "env", "access_token": "token"}

    respx.post(
        "https://api.twitter.com/1.1/account_activity/all/env/subscriptions.json"
    ).mock(return_value=Response(status_code=204))

    async with client:
        resp: Response = await client.post("/webhook/twitter/subscriptions", json=body)
        assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_check_subscription(client):
    params = {"env": "env", "access_token": "token"}
    respx.get(
        "https://api.twitter.com/1.1/account_activity/all/env/subscriptions.json"
    ).mock(return_value=Response(status_code=204))

    async with client:
        resp: Response = await client.get(
            "/webhook/twitter/subscriptions", params=params
        )
        assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_delete_subscription(client):
    params = {"env": "env", "user_id": "1"}

    respx.delete(
        "https://api.twitter.com/1.1/account_activity/all/env/subscriptions/1.json"
    ).mock(return_value=Response(status_code=204))

    async with client:
        resp: Response = await client.delete(
            "/webhook/twitter/subscriptions", params=params
        )
        assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_list_subscriptions(client):
    params = {"env": "env"}
    data = {
        "environment": "appname",
        "application_id": "13090192",
        "subscriptions": [{"user_id": "3001969357"}],
    }
    respx.get(
        "https://api.twitter.com/1.1/account_activity/all/env/subscriptions/list.json"
    ).mock(return_value=Response(status_code=200, json=data))

    async with client:
        resp: Response = await client.get(
            "/webhook/twitter/subscriptions/list", params=params
        )
        assert resp.status_code == 200
        assert resp.json()["environment"] == "appname"


@respx.mock
@pytest.mark.asyncio
async def test_subscriptions_count(client):
    data = {
        "account_name": "my-account",
        "subscriptions_count": "1",
        "provisioned_count": "25",
    }
    respx.get(
        "https://api.twitter.com/1.1/account_activity/all/subscriptions/count.json"
    ).mock(return_value=Response(status_code=200, json=data))
    async with client:
        resp: Response = await client.get("/webhook/twitter/subscriptions/count")
        assert resp.status_code == 200
        assert resp.json()["subscriptions_count"] == "1"
