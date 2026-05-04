"""Batch file download handler for Save Restricted Content Bot.

This module handles the /get_batch command which allows users to download
multiple files in batch from multiple Telegram post URLs.
"""

from typing import cast

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from app.core.config import DOWNLOAD_DIR
from app.core.logger import log
from app.core.user import user_client
from app.services.download_service import download_message_media
from app.services.parser_service import parse_batch_telegram_post_urls
from app.utils.batch_log import update_batch_log

# Track users waiting for URL input for /get_batch command
pending_get_users: dict[int, bool] = {}


def register_get_batch_file_handler(bot: TelegramClient) -> None:
    """Register the /get_batch command handler for batch downloads.

    Args:
        bot (TelegramClient): The bot client instance.
    """

    @bot.on(events.NewMessage(pattern=r"^/get_batch$"))
    async def get_batch(event):
        """Handle /get_batch command.

        Marks the user as waiting for URL list input and prompts them
        to send Telegram post URLs (one per line).

        Args:
            event: The NewMessage event from Telethon.
        """
        user_id = event.sender_id

        pending_get_users[user_id] = True

        log.info("Triggered /get_batch command by user", "Handlers")
        await event.respond(
            "📥 Ready for batch download.\\n\\n"
            "Please send the Telegram post URLs.\\n\\n"
            "🔗 Example:\\n"
            "`https://t.me/c/3776460651/123`\\n\\n"
            "I'll extract the posts and begin downloading them."
        )

    @bot.on(events.NewMessage())
    async def receive_post_urls(event):
        """Handle batch URL submission.

        Receives multiple Telegram post URLs (one per line), validates them,
        fetches messages, downloads media in batch, and reports progress.

        Args:
            event: The NewMessage event from Telethon.
        """
        user_id = event.sender_id

        if not pending_get_users.get(user_id):
            return

        if not event.raw_text:
            return

        if event.raw_text.startswith("/"):
            return

        posts_url = event.raw_text.strip()

        log.info("Received batch URL input:", "Handlers")
        for line in posts_url.splitlines():
            clean_line = line.strip()
            if clean_line:
                log.info(f"  └─ {clean_line}", "Handlers")

        try:
            parsed_urls = parse_batch_telegram_post_urls(posts_url)
            pending_get_users[user_id] = False

            log.info("Parsed batch URLs successfully:", "Handlers")
            for _, message_id, original_url in parsed_urls:
                log.info(
                    f"  └─ Message ID {message_id}: {original_url}",
                    "Handlers",
                )

        except Exception as e:
            error_msg = str(e)
            log.error(f"Batch URL parsing failed: {error_msg}", "Handlers")
            await event.respond(
                "❌ Invalid input.\\n\\n"
                f"Reason: {error_msg}\\n\\n"
                "Please send valid Telegram post URLs, one per line."
            )
            return

        total_posts = len(parsed_urls)

        progress_msg = await event.respond("⏳ Preparing batch download...")

        progress_log_msg = await event.respond(
            "Downloaded Posts:\\n\\n⏳ No completed downloads yet..."
        )

        log_entries: list[str] = []
        success_count = 0

        for index, (channel_id, message_id, original_url) in enumerate(
            parsed_urls, start=1
        ):
            try:
                log.info(
                    f"[{index}/{total_posts}] Fetching message: "
                    f"channel_id={channel_id}, message_id={message_id}",
                    "Handlers",
                )

                raw_message = await user_client.get_messages(
                    entity=channel_id,
                    ids=message_id,
                )

                if not raw_message:
                    raise ValueError("Message not found")

                if isinstance(raw_message, list):
                    if not raw_message:
                        raise ValueError("Message not found")
                    raw_message = raw_message[0]

                telegram_message = cast(Message, raw_message)

                saved_path = await download_message_media(
                    bot=bot,
                    chat_id=event.chat_id,
                    message_id=progress_msg.id,
                    message=telegram_message,
                    download_dir=DOWNLOAD_DIR,
                    progress_prefix=f"Downloading {index}/{total_posts} posts...",
                )

                success_count += 1

                entry = (
                    f"Post {index} (Message ID: {message_id}):\\n\\n"
                    f"✅ Download Complete!\\n\\n"
                    f"📁 Saved to:\\n"
                    f"{saved_path}\\n\\n"
                    f"{'─' * 40}"
                )

                log_entries.append(entry)

                await update_batch_log(
                    bot=bot,
                    chat_id=event.chat_id,
                    message_id=progress_log_msg.id,
                    entries=log_entries,
                )

                log.info(
                    f"[{index}/{total_posts}] Post downloaded successfully: "
                    f"message_id={message_id}, path={saved_path}",
                    "Handlers",
                )

            except Exception as e:
                error_message = str(e)

                log.error(
                    f"[{index}/{total_posts}] Failed to download post: "
                    f"message_id={message_id}, url={original_url}, "
                    f"error={error_message}",
                    "Handlers",
                )

                entry = (
                    f"Post {index} (Message ID: {message_id}):\\n\\n"
                    f"❌ Download Failed!\\n\\n"
                    f"🔗 URL:\\n"
                    f"{original_url}\\n\\n"
                    f"Reason:\\n"
                    f"{error_message}\\n\\n"
                    f"{'─' * 40}"
                )

                log_entries.append(entry)

                await update_batch_log(
                    bot=bot,
                    chat_id=event.chat_id,
                    message_id=progress_log_msg.id,
                    entries=log_entries,
                )

        await bot.edit_message(
            event.chat_id,
            progress_msg.id,
            f"✅ Batch download completed!\\n\\n"
            f"Downloaded {success_count}/{total_posts} posts successfully.",
        )

        log.info(
            f"Batch download completed: {success_count}/{total_posts} posts downloaded",
            "Handlers",
        )
