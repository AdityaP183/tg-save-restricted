# Changelog

All notable changes to the Save Restricted Content Bot project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-05-04

### Added

- Initial release of the Telegram Save Restricted Content Bot
- `/start` command for welcome message and introduction
- `/help` command for listing available commands
- `/get` command to download a single Telegram post media
- `/get_batch` command to download multiple posts in batch
- Telethon-based user client integration for accessing restricted/private channels
- Session-based authentication using Telegram user session string
- Download service with real-time progress tracking (percentage, speed, ETA)
- Message service for fetching Telegram messages
- URL parser service for extracting channel and message IDs
- Validation utilities for Telegram URL format checking
- Batch processing with duplicate URL detection
- Structured logging system with file and console output
- Progress display utilities for user feedback
- Modular project architecture (core, handlers, services, utils)
- Environment configuration using `.env` file
- Session generation script (`get_session.py`)
- Log storage system under `data/logs/`
