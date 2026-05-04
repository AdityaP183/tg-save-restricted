"""User session management module for Save Restricted Content Bot.

This module initializes and manages the Telegram user client using
a session string. The user client is used to download media from
private channels and restricted content.

The session string must be provided via the SESSION_STRING environment
variable. This represents an authenticated Telegram user session.
"""

from telethon import TelegramClient
from telethon.sessions import StringSession

from app.core.config import API_HASH, API_ID, SESSION_STRING

if not SESSION_STRING:
    raise ValueError(
        "SESSION_STRING is missing in .env. "
        "Please generate a session string first using generate_session_string.py"
    )

# Initialize the user client with authenticated session
user_client: TelegramClient = TelegramClient(
    StringSession(SESSION_STRING), API_ID, API_HASH
)
"""Global TelegramClient instance for authenticated user operations."""
