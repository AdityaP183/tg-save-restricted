"""Start command handler for Save Restricted Content Bot.

This module handles the /start command which provides a welcome message
to users.
"""

from telethon import TelegramClient, events

from app.core.logger import log


def register_start_handler(bot: TelegramClient) -> None:
    """Register the /start command handler.

    Args:
        bot (TelegramClient): The bot client instance.
    """

    @bot.on(events.NewMessage(pattern=r"^/start$"))
    async def start(event):
        """Handle /start command.

        Sends a welcome message with information about the bot's
        capabilities to the user.

        Args:
            event: The NewMessage event from Telethon.
        """
        log.info("Triggered /start command by user", "Handlers")
        await event.respond(
            "👋 **Welcome to Save Restricted Content Bot**\n\n"
            "I can help you save files from Telegram links using your connected account.\n\n"
            "📌 **What I can do:**\n"
            "• Download a single file\n"
            "• Download multiple files in batch\n\n"
            "Use /help to see all available commands."
        )
