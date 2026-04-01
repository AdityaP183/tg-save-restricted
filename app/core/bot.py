from telethon import TelegramClient

from app.core.config import API_HASH, API_ID, BOT_TOKEN
from app.core.logger import log
from app.handlers.start_handler import register_start_handler


def run_bot():
    bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    log.info("Bot started running...", "Bot")

    register_start_handler(bot)

    bot.run_until_disconnected()
