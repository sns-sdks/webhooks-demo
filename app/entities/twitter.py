"""
    Data model for twitter
"""
from typing import Optional

from pydantic import BaseModel


class Payload(BaseModel):
    for_user_id: str
    is_blocked_by: Optional[bool] = None
    tweet_create_events: Optional[dict] = None
    favorite_events: Optional[dict] = None
    follow_events: Optional[dict] = None
    unfollow_events: Optional[dict] = None
    block_events: Optional[dict] = None
    unblock_events: Optional[dict] = None
    mute_events: Optional[dict] = None
    unmute_events: Optional[dict] = None
    user_event: Optional[dict] = None
    direct_message_events: Optional[dict] = None
    direct_message_indicate_typing_events: Optional[dict] = None
    direct_message_mark_read_events: Optional[dict] = None
    tweet_delete_events: Optional[dict] = None
