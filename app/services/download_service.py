import asyncio
import os
import time
from typing import cast

from telethon.hints import MessageLike
from telethon.tl.custom.message import Message

from app.core.logger import log
from app.core.user import user_client
from app.utils.show_progress import show_progress


async def download_message_media(
    *,
    bot,
    chat_id: int,
    message_id: int,
    message: Message,
    download_dir: str,
    progress_prefix: str = "⬇️ Downloading file...",
) -> str | bytes:
    """
    Downloads media from a Telegram message.

    Returns:
        downloaded file path
    """

    if not message.media:
        raise ValueError("This post does not contain downloadable media")

    os.makedirs(download_dir, exist_ok=True)

    start_time = time.time()

    progress_state = {
        "current": 0,
        "total": message.file.size if message.file and message.file.size else 1,
        "done": False,
    }

    async def progress_updater():
        last_percent = -1
        while not progress_state["done"]:
            try:
                percent = int(
                    (progress_state["current"] / progress_state["total"]) * 100
                )

                if percent != last_percent:
                    last_percent = percent
                    await show_progress(
                        bot=bot,
                        chat_id=chat_id,
                        message_id=message_id,
                        current=progress_state["current"],
                        total=progress_state["total"],
                        start_time=start_time,
                        prefix=progress_prefix,
                    )

            except Exception as e:
                log.error(f"Progress updater failed: {str(e)}", "DownloadService")

            await asyncio.sleep(1)

        await show_progress(
            bot=bot,
            chat_id=chat_id,
            message_id=message_id,
            current=progress_state["total"],
            total=progress_state["total"],
            start_time=start_time,
            prefix=progress_prefix,
        )

    def progress_callback(current: int, total: int) -> None:
        progress_state["current"] = current
        progress_state["total"] = total

    updater_task = asyncio.create_task(progress_updater())

    try:
        file_path = await user_client.download_media(
            cast(MessageLike, message),
            file=download_dir,
            progress_callback=progress_callback,
        )

        if not file_path:
            raise ValueError("Download failed or returned empty file path")

        progress_state["done"] = True
        await updater_task

        log.info(f"Downloaded file successfully -> {file_path}", "DownloadService")

        return file_path

    except Exception:
        progress_state["done"] = True
        await updater_task
        raise
