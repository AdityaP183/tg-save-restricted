"""Single file download handler for Save Restricted Content Bot.

This module handles the /get command which allows users to download
a single file from a Telegram post URL.
"""

from telethon import TelegramClient, events

from app.core.config import DOWNLOAD_DIR
from app.core.logger import log
from app.services.download_service import download_message_media
from app.services.message_service import fetch_message
from app.services.parser_service import parse_telegram_post_url
from app.utils.validators import is_valid_telegram_post_url

pending_get_users: dict[int, bool] = {}


def register_get_file_handler(bot: TelegramClient) -> None:
    """Register the /get command handler for single file downloads.

    Args:
        bot (TelegramClient): The bot client instance.
    """

    @bot.on(events.NewMessage(pattern=r"^/get$"))
    async def get(event):
        """Handle /get command.

        Marks the user as waiting for a post URL and prompts them to send it.

        Args:
            event: The NewMessage event from Telethon.
        """
        user_id = event.sender_id

        pending_get_users[user_id] = True

        log.info("Triggered /get command by user", "Handlers")
        await event.respond("📩 Please share the post URL")

    @bot.on(events.NewMessage())
    async def receive_post_url(event):
        """Handle post URL submission.

        Receives and validates a Telegram post URL, fetches the message,
        downloads the media, and sends the result back to the user.

        Args:
            event: The NewMessage event from Telethon.
        """
        user_id = event.sender_id
        text = event.raw_text.strip()

        if user_id not in pending_get_users:
            return

        if text.startswith("/"):
            return

        if not is_valid_telegram_post_url(text):
            log.warning(
                f"Invalid URL format received: {text}",
                "Handlers",
            )
            await event.respond(
                "❌ Invalid Telegram post URL.\n\n"
                "Please send a valid link like:\n"
                '"`https://t.me/c/3776460651/4`"'
            )
            return

        try:
            channel_id, message_id = parse_telegram_post_url(text)

            log.info(
                f"Parsed URL -> channel_id={channel_id}, message_id={message_id}",
                "Handlers",
            )

            progress_message = await event.respond("🔍 Fetching Telegram post...")

            message = await fetch_message(channel_id, message_id)

            await progress_message.edit("🚀 Starting download...")

            file_path = await download_message_media(
                bot=bot,
                chat_id=event.chat_id,
                message_id=progress_message.id,
                message=message,
                download_dir=DOWNLOAD_DIR,
            )

            pending_get_users.pop(user_id, None)

            await bot.edit_message(
                event.chat_id,
                progress_message.id,
                f"✅ Download Complete!\n\n📁 Saved to:\n`{file_path}`",
            )

            log.info("Single file download completed successfully", "Handlers")

        except Exception as e:
            pending_get_users.pop(user_id, None)

            error_msg = str(e)
            log.error(f"/get command failed: {error_msg}", "Handlers")
            await event.respond(f"❌ Download failed:\n`{error_msg}`")
