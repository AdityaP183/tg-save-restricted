# tg-save-restricted

```
telegram-downloader/                  # Project root
│
├── app/                              # Main app package
│   ├── __init__.py                   # Package marker
│   │
│   ├── core/                         # Core app setup
│   │   ├── __init__.py               # Package marker
│   │   ├── config.py                 # Env config loader
│   │   ├── client.py                 # Telethon client setup
│   │   └── logger.py                 # App logging setup
│   │
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py               # Package marker
│   │   ├── auth_service.py           # Session/auth operations
│   │   ├── parser_service.py         # Telegram link parser
│   │   ├── download_service.py       # File download logic
│   │   ├── message_service.py        # Telegram message fetch
│   │   └── file_service.py           # File handling helpers
│   │
│   ├── handlers/                     # User interaction flow
│   │   ├── __init__.py               # Package marker
│   │   └── cli_handler.py            # Main menu interface
│   │
│   ├── models/                       # Structured data models
│   │   ├── __init__.py               # Package marker
│   │   ├── download_item.py          # Parsed download input
│   │   └── download_result.py        # Download result model
│   │
│   ├── storage/                      # Local data storage
│   │   ├── __init__.py               # Package marker
│   │   ├── db.py                     # SQLite connection/init
│   │   └── queue_repo.py             # Batch queue storage
│   │
│   └── utils/                        # Small reusable helpers
│       ├── __init__.py               # Package marker
│       ├── formatters.py             # Size/time formatting
│       ├── validators.py             # Input validation helpers
│       └── progress.py               # Progress display logic
│
├── data/                             # Runtime app data
│   ├── app.db                        # SQLite database file
│   ├── downloads/                    # Downloaded file output
│   └── logs/                         # Log file storage
│
├── main.py                           # App entry point
├── .env                              # User config values
├── .gitignore                        # Git ignored files
├── pyproject.toml                    # Project dependencies
└── README.md                         # Setup and usage guide


/start - Welcome msg and other stuff
/help - List of commands
/login - as session.string is not available on first run it will login in user generate session string file, if all the env is there then direct login
/me - User info
/logout
/set_dir - set download directory locally
/get - single item download
/get_batch
