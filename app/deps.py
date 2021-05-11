from authlib.integrations.httpx_client import AsyncOAuth1Client
from httpx import AsyncClient

import config

tw_cli = AsyncOAuth1Client(
    client_id=config.TWITTER_CONSUMER_KEY,
    client_secret=config.TWITTER_CONSUMER_SECRET,
    token=config.TWITTER_ACCESS_TOKEN,
    token_secret=config.TWITTER_ACCESS_SECRET,
)

fb_cli = AsyncClient()
