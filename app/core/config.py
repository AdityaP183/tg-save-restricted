import os

from dotenv import load_dotenv

load_dotenv(".env")

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")
