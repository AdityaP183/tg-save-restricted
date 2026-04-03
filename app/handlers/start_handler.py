from telethon import TelegramClient, events

from app.core.logger import log


def register_start_handler(bot: TelegramClient):
    @bot.on(events.NewMessage(pattern=r"^/start$"))
    async def start(event):
        log.info("Triggered /start command by user", "Handlers")
        await event.respond(
            "👋 **Welcome to Save Restricted Content Bot**\n\n"
            "I can help you save files from Telegram links using your connected account.\n\n"
            "📌 **What I can do:**\n"
            "• Download a single file\n"
            "• Download multiple files in batch\n\n"
            "Use /help to see all available commands."
        )
