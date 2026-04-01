from telethon import TelegramClient, events


def register_start_handler(bot: TelegramClient):
    @bot.on(events.NewMessage(pattern=r"^/start$"))
    async def start(event):
        await event.respond(
            "👋 **Welcome to Save Restricted Content Bot**\n\n"
            "I can help you save files from Telegram links using your connected account.\n\n"
            "📌 **What I can do:**\n"
            "• Download a single file\n"
            "• Download multiple files in batch\n"
            "• Manage your login session\n"
            "• Set your local download directory\n\n"
            "⚡ **Quick Start:**\n"
            "1. Use `/login` to connect your Telegram account\n"
            "2. Use `/set_dir` to choose where files will be saved\n"
            "3. Use `/get` or `/get_batch` to download files\n\n"
            "📖 Use `/help` to see all available commands."
        )
