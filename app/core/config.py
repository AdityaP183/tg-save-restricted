"""Configuration module for Save Restricted Content Bot.

This module loads environment variables from a .env file and exposes them
as module-level constants. These are used throughout the application for
Telegram API authentication and download settings.

Required environment variables (in .env):
    - API_ID: Your Telegram API ID
    - API_HASH: Your Telegram API hash
    - BOT_TOKEN: Your Telegram bot token
    - SESSION_STRING: Your Telegram user session string
    - DOWNLOAD_DIR: Directory to save downloaded files
"""

import os

from dotenv import load_dotenv

load_dotenv(".env")

API_ID: int = int(os.getenv("API_ID", "0"))
"""Telegram API ID from my.telegram.org"""

API_HASH: str = os.getenv("API_HASH", "")
"""Telegram API hash from my.telegram.org"""

# Bot and user authentication
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
"""Telegram bot token from BotFather"""

SESSION_STRING: str = os.getenv("SESSION_STRING", "")
"""Telegram user session string for authenticated downloads"""

# Download settings
DOWNLOAD_DIR: str = os.getenv("DOWNLOAD_DIR", "./")
"""Directory where downloaded files will be saved"""
