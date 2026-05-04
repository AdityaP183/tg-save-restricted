"""Batch log utility module for Save Restricted Content Bot.

This module provides utilities for updating batch download progress
messages in Telegram.
"""

from app.core.logger import log


async def update_batch_log(
    *,
    bot,
    chat_id: int,
    message_id: int,
    entries: list[str],
) -> None:
    """Update the batch download progress message.

    Edits a Telegram message to display the current state of batch
    downloads with download entries. Handles "message was not modified"
    errors gracefully.

    Args:
        bot: The bot client instance for editing messages.
        chat_id (int): The chat ID where the message is located.
        message_id (int): The message ID to edit.
        entries (list[str]): List of download status entries to display.
    """
    if not entries:
        text = "Downloaded Posts:\\n\\n⏳ No completed downloads yet..."
    else:
        text = "Downloaded Posts:\\n\\n" + "\\n\\n".join(entries)

    try:
        await bot.edit_message(chat_id, message_id, text)
    except Exception as e:
        err = str(e).lower()

        if (
            "message was not modified" in err
            or "content of the message was not modified" in err
        ):
            return

        log.error(f"Batch log update failed: {str(e)}", "BatchLog")
