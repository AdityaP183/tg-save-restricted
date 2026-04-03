from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from app.core.config import API_HASH, API_ID


def main() -> None:
    if not API_ID or not API_HASH:
        raise ValueError("API_ID or API_HASH is missing in your .env file")

    print("=== Telegram Session String Generator ===\n")
    print("You will be asked to log in with your Telegram account.\n")

    with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        session_string = client.session.save()

        print("\n✅ Session string generated successfully!\n")
        print("Paste this into your .env file:\n")
        print(f'SESSION_STRING="{session_string}"\n')


if __name__ == "__main__":
    main()
