from telethon import TelegramClient
from telethon.sessions import StringSession

from app.core.config import API_HASH, API_ID, SESSION_STRING

if not SESSION_STRING:
    raise ValueError("SESSION_STRING is missing in .env")

user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
