# tg-save-restricted

A Telegram bot built with **Telethon** to save restricted/private Telegram media using your own logged-in user session.

This bot allows you to:

- 📥 Download media from Telegram post links
- 💾 Save files locally to your PC
- 🔐 Use your own Telegram account access for joined/private channels
- 📦 Batch download multiple files at once
- ⚡ Real-time progress tracking with speed and ETA

## Table of Contents

- [Requirements](#requirements)
- [Project Setup](#project-setup)
- [Getting Telegram Credentials](#getting-telegram-credentials)
- [Running the Bot](#running-the-bot)
- [Bot Commands](#bot-commands)
- [Usage Examples](#usage-examples)
- [Logging](#logging)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- **Python** 3.12+
- **[Telethon](https://github.com/LonamiWebs/Telethon)** - Python Telegram client library
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management
- **[cryptg](https://pypi.org/project/cryptg/)** - Faster Telegram downloads (optional but recommended)
- **[uv](https://docs.astral.sh/uv/)** - Python package manager

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/tg-save-restricted.git
cd tg-save-restricted
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

> **Note**: `cryptg` is included for faster Telegram downloads. If installation fails, the bot will still work but downloads may be slower.

### 3. Create Environment File

Create a `.env` file in the project root directory:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
SESSION_STRING=your_user_session_string
DOWNLOAD_DIR=download_directory
```

See [Getting Telegram Credentials](#getting-telegram-credentials) for how to obtain these values.

### 4. Generate User Session String

Before running the bot, you need to generate a user session string:

```bash
uv run get_session.py
```

This will prompt you to:

1. Enter your Telegram phone number
2. Enter the verification code you receive
3. Save the generated session string to your `.env` file as `SESSION_STRING`

## Getting Telegram Credentials

### Step 1: Get API ID & API Hash

1. Go to https://my.telegram.org
2. Log in with your Telegram account
3. Click on "API development tools"
4. Create a new application or use existing one
5. Copy your `API_ID` and `API_HASH`

```env
API_ID=123456789
API_HASH=abcdef1234567890abcdef1234567890
```

### Step 2: Create Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the prompts to create a new bot
4. Copy the bot token from the response

```env
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

### Step 3: Generate Session String

Run the session string generator:

```bash
uv run generate_session_string.py
```

Follow the prompts and save the generated string:

```env
SESSION_STRING="1BVtsOH5u7x_your_session_string_here_abcdef1234567890..."
```

### Step 4: Set Download Directory

Specify where files should be saved:

```env
DOWNLOAD_DIR=D:/Downloads/Telegram
```

Or use a relative path:

```env
DOWNLOAD_DIR=./downloads
```

## Running the Bot

Start the bot:

```bash
uv run main.py
```

You should see output like:

```
[2024-01-15 10:30:45] [INFO] [Bot] Bot started running...
[2024-01-15 10:30:46] [INFO] [Bot] User client connected successfully
```

The bot is now running and ready to receive commands!

## Bot Commands

### `/start`

- **Description**: Welcome message and quick introduction
- **Usage**: Send `/start` to the bot
- **Response**: Welcome message with bot capabilities

### `/help`

- **Description**: Show all available commands
- **Usage**: Send `/help` to the bot
- **Response**: Detailed command reference

### `/get`

- **Description**: Download a single file from a Telegram post
- **Usage**:
    1. Send `/get`
    2. Reply with a Telegram post URL
- **URL Format**: `https://t.me/c/CHANNEL_ID/MESSAGE_ID`
- **Example**:
    ```
    /get
    https://t.me/c/3776460651/42
    ```

### `/get_batch`

- **Description**: Download multiple files in batch
- **Usage**:
    1. Send `/get_batch`
    2. Reply with multiple URLs (one per line)
- **Example**:
    ```
    /get_batch
    https://t.me/c/3776460651/40
    https://t.me/c/3776460651/41
    https://t.me/c/3776460651/42
    ```
- **Features**:
    - Automatically skips duplicate URLs
    - Shows progress for each download
    - Displays final report with success count

## Logging

The bot logs all activities to both console and file.

### Log Files

Logs are saved in the `data/logs/` directory with timestamps:

```
data/logs/
├── 2024-01-15_10-30-45.log
├── 2024-01-15_14-22-18.log
└── ...
```

### Log Levels

- **INFO** - Regular operations and milestones
- **WARNING** - Unusual but recoverable situations
- **ERROR** - Errors and failures

### Log Format

```
[2024-01-15 10:30:45] [INFO] [Bot] Bot started running...
[2024-01-15 10:30:46] [INFO] [DownloadService] Downloaded file successfully -> /path/to/file
[2024-01-15 10:35:12] [ERROR] [Handlers] /get command failed: Invalid URL format
```

## Architecture

### Directory Structure

```
tg-save-restricted/
├── app/
│   ├── core/                    # Core bot functionality
│   │   ├── bot.py              # Bot initialization and lifecycle
│   │   ├── config.py           # Configuration loading
│   │   ├── logger.py           # Logging system
│   │   └── user.py             # User session management
│   ├── handlers/               # Command handlers
│   │   ├── start_handler.py
│   │   ├── help_handler.py
│   │   ├── get_file_handler.py
│   │   └── get_batch_file_handler.py
│   ├── services/               # Business logic
│   │   ├── download_service.py  # Download with progress
│   │   ├── message_service.py   # Message fetching
│   │   └── parser_service.py    # URL parsing
│   └── utils/                  # Utilities
│       ├── validators.py        # URL validation
│       ├── batch_log.py         # Batch progress display
│       └── show_progress.py     # Progress formatting
├── data/
│   └── logs/                    # Log files (created at runtime)
├── main.py                      # Application entry point
├── README.md                    # This file
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Project history
├── pyproject.toml              # Project metadata
└── LICENSE                     # MIT License
```

### Flow Diagram

```
User Message
    ↓
Handler (Parses command)
    ↓
Parser Service (Extracts URL/IDs)
    ↓
Message Service (Fetches from Telegram)
    ↓
Download Service (Downloads with progress)
    ↓
Progress Display (Updates user in real-time)
    ↓
Response (Success or error message)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code style guidelines
- How to set up a development environment
- How to test your changes
- Pull request process

Quick reference:

- Add type hints to all functions
- Include comprehensive docstrings
- Use the logging system consistently
- Test all changes before submitting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs in `data/logs/`
3. Check existing issues on GitHub
4. Create a new issue with:
    - What you were trying to do
    - The exact error message
    - Your OS and Python version
    - Relevant log entries (without sensitive data)
