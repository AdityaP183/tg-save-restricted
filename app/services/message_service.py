from telethon.tl.custom.message import Message

from app.core.logger import log
from app.core.user import user_client


async def fetch_message(channel_id: int, message_id: int) -> Message:
    """
    Fetches a Telegram message using the user client.
    """

    message = await user_client.get_messages(channel_id, ids=message_id)

    if not isinstance(message, Message):
        raise ValueError("Expected a single Telegram message, but got something else")

    log.info(
        f"Fetched message successfully (channel_id={channel_id}, message_id={message_id})",
        "MessageService",
    )

    return message
