import pytest
import respx
from httpx import AsyncClient, Response

from app.main import app


@pytest.mark.asyncio
async def test_verify_challenge():
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": "meatyhamhock",
        "hub.challenge": "1158201444",
    }
    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.get("/facebook", params=params)
        assert resp.status_code == 200
        assert resp.text == "hello"


@pytest.mark.asyncio
async def test_webhook_event():
    payload = {
        "entry": [
            {
                "time": 1520383571,
                "changes": [
                    {
                        "field": "photos",
                        "value": {"verb": "update", "object_id": "10211885744794461"},
                    }
                ],
                "id": "10210299214172187",
            }
        ],
        "object": "user",
    }

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.post("/facebook", json=payload)
        assert resp.status_code == 200
        assert resp.text == "ok"


@respx.mock
@pytest.mark.asyncio
async def test_subscribe_webhook():
    page_id = "123456789"
    body = {"page_id": page_id, "fields": "feed,videos", "access_token": "token"}
    respx.post(f"https://graph.facebook.com/{page_id}/subscribed_apps").mock(
        return_value=Response(status_code=200, json={"success": "true"})
    )

    async with AsyncClient(app=app, base_url="https://test") as ac:
        resp: Response = await ac.post("/facebook/subscribed_apps", json=body)
        assert resp.status_code == 200
        assert resp.json()["success"] == "true"
