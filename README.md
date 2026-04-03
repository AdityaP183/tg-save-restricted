# tg-save-restricted

A Telegram bot built with **Telethon** to save restricted/private Telegram media using your own logged-in user session.

This bot allows you to:
- Download media from Telegram post links
- Save files locally to your PC
- Use your own Telegram account access for joined/private channels

---

## Tech Stack

- Python 3.12+
- [Telethon](https://github.com/LonamiWebs/Telethon)
- [uv](https://docs.astral.sh/uv/)

---

## Project Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/tg-save-restricted.git
cd tg-save-restricted
```

### 2. Install dependencies with uv

```bash
uv sync
```

> Recommended: `cryptg` is included for faster Telegram downloads.

---

## Environment Variables

Create a `.env` file in the project root:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
SESSION_STRING=your_user_session_string
DOWNLOAD_DIR=D:/Downloads/Telegram
```

---

## Getting Telegram Credentials

### Telegram API ID & API HASH
Get them from:
https://my.telegram.org

### Bot Token
Create a bot using:
[@BotFather](https://t.me/BotFather)

### Generate Session String

Before using the bot, generate your Telegram user session string:

```bash
uv run .\generate_session_string.py
```

Then copy the output and paste it into your `.env` file:

```env
SESSION_STRING="your_generated_session_string"
```

---

## Run the Bot

```bash
uv run .\main.py
```

---

## Bot Commands

```txt
/start      - Start bot / check status
/help       - Help and usage guide
/get        - Download one file
```
---

## Example Flow

1. Start the bot
2. Use `/get`
3. Send a Telegram post URL like:

```txt
https://t.me/c/3776460651/6
```

4. Bot fetches the file
5. Download starts with progress updates
6. File is saved locally

---

## Notes

- This bot works using **your own Telegram user session**
- You must already have access to the private/restricted channel/group
- Download speed depends on Telegram routing, your internet, and local system performance

---

## License

MIT
