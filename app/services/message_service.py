"""Message service module for Save Restricted Content Bot.

This module handles fetching Telegram messages from channels
using the authenticated user client.
"""

from telethon.tl.custom.message import Message

from app.core.logger import log
from app.core.user import user_client


async def fetch_message(channel_id: int, message_id: int) -> Message:
    """Fetch a Telegram message from a channel.

    This function retrieves a single message from a Telegram channel using
    the authenticated user client. It validates that the returned object
    is a Message instance.

    Args:
        channel_id (int): The internal Telegram channel ID
            (e.g., -1003776460651).
        message_id (int): The message/post ID to retrieve.

    Returns:
        Message: The Telegram message object containing media and metadata.

    Raises:
        ValueError: If the returned object is not a Message instance
            or if the message is not found.

    Example:
        >>> message = await fetch_message(-1003776460651, 42)
        >>> print(message.text)
    """

    message = await user_client.get_messages(channel_id, ids=message_id)

    if not isinstance(message, Message):
        raise ValueError("Expected a single Telegram message, but got something else")

    log.info(
        f"Fetched message successfully (channel_id={channel_id}, message_id={message_id})",
        "MessageService",
    )

    return message
