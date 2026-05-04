"""Validators module for Save Restricted Content Bot.

This module provides URL validation functions to ensure that user-provided
URLs match the expected Telegram post URL format.
"""

import re


def is_valid_telegram_post_url(url: str) -> bool:
    """Validate if a string is a valid Telegram private channel post URL.

    Checks if the URL matches the format:
    https://t.me/c/<channel_id>/<message_id>

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Example:
        >>> is_valid_telegram_post_url("https://t.me/c/3776460651/4")
        True
        >>> is_valid_telegram_post_url("https://t.me/channel_name/4")
        False
    """
    pattern = r"^https:\/\/t\.me\/c\/\d+\/\d+$"
    return bool(re.match(pattern, url.strip()))
