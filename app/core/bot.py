from telethon import TelegramClient

from app.core.config import API_HASH, API_ID, BOT_TOKEN
from app.core.logger import log
from app.core.user import user_client
from app.handlers.get_file_handler import register_get_file_handler
from app.handlers.help_handler import register_help_handler
from app.handlers.start_handler import register_start_handler


async def run_bot() -> None:
    bot = TelegramClient("bot_session", API_ID, API_HASH)
    await bot.start(bot_token=BOT_TOKEN)  # type: ignore

    await user_client.connect()

    register_start_handler(bot)
    register_help_handler(bot)
    register_get_file_handler(bot)

    log.info("Bot started running...", "Bot")
    log.info("User client connected successfully", "Bot")

    try:
        await bot.run_until_disconnected()  # type: ignore
    finally:
        await user_client.disconnect()  # type: ignore
        await bot.disconnect()  # type: ignore
        log.info("Bot shutdown completed", "Bot")
