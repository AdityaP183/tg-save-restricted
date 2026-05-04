"""Help command handler for Save Restricted Content Bot.

This module handles the /help command which lists all available
commands and their descriptions.
"""

from telethon import TelegramClient, events

from app.core.logger import log


def register_help_handler(bot: TelegramClient) -> None:
    """Register the /help command handler.

    Args:
        bot (TelegramClient): The bot client instance.
    """

    @bot.on(events.NewMessage(pattern=r"^/help$"))
    async def help(event):
        """Handle /help command.

        Sends a message listing all available commands and their descriptions.

        Args:
            event: The NewMessage event from Telethon.
        """
        log.info("Triggered /help command by user", "Handlers")
        await event.respond(
            "🛠 **Save Restricted Content Bot — Commands**\n\n"
            "Use the commands below to manage your session and download files.\n\n"
            "🚀 **General**\n"
            "/start — Welcome message and quick intro\n"
            "/help — Show all available commands\n\n"
            "⬇️ **Download Commands**\n"
            "/get — Download a single file from a Telegram post link\n"
            "⚠️ You must already have access to the target Telegram channel/post."
        )
