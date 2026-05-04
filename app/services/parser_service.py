"""Parser service module for Save Restricted Content Bot.

This module handles parsing of Telegram post URLs and extracting
channel IDs and message IDs from them.
"""

import re


def parse_telegram_post_url(url: str) -> tuple[int, int]:
    """Parse a Telegram private channel post URL.

    Parses Telegram private channel post URLs of the format:
    https://t.me/c/3776460651/4

    The channel ID is converted to the internal Telegram format
    by prefixing with -100.

    Args:
        url (str): The Telegram post URL to parse.

    Returns:
        tuple[int, int]: A tuple of (channel_id, message_id)
            where channel_id is in the internal format (e.g., -1003776460651)
            and message_id is the post number.

    Raises:
        ValueError: If the URL format is invalid.

    Example:
        >>> parse_telegram_post_url("https://t.me/c/3776460651/4")
        (-1003776460651, 4)
    """

    pattern = r"^https:\/\/t\.me\/c\/(\d+)\/(\d+)$"
    match = re.match(pattern, url.strip())

    if not match:
        raise ValueError("Invalid Telegram post URL format")

    raw_channel_id = match.group(1)
    message_id = int(match.group(2))

    channel_id = int(f"-100{raw_channel_id}")

    return channel_id, message_id


def parse_batch_telegram_post_urls(raw_text: str) -> list[tuple[int, int, str]]:
    """Parse multiple Telegram post URLs from multiline text.

    This function parses multiple Telegram post URLs from a block of text,
    one URL per line. It automatically removes duplicates and validates
    each URL.

    Args:
        raw_text (str): Multi-line text containing Telegram post URLs,
            one per line. Empty lines are ignored.

    Returns:
        list[tuple[int, int, str]]: List of tuples containing:
            - channel_id (int): Internal Telegram channel ID
            - message_id (int): Telegram message/post ID
            - original_url (str): The original URL string

    Raises:
        ValueError: If no valid URLs are found in the input.

    Example:
        >>> urls = parse_batch_telegram_post_urls(
        ...     "https://t.me/c/3776460651/20\\n"
        ...     "https://t.me/c/3776460651/21\\n"
        ... )
        >>> len(urls)
        2
        >>> urls[0]
        (-1003776460651, 20, 'https://t.me/c/3776460651/20')
    """
    parsed_urls: list[tuple[int, int, str]] = []
    seen: set[tuple[int, int]] = set()

    for line in raw_text.splitlines():
        url = line.strip()

        if not url:
            continue

        channel_id, message_id = parse_telegram_post_url(url)

        key = (channel_id, message_id)
        if key in seen:
            continue

        seen.add(key)
        parsed_urls.append((channel_id, message_id, url))

    if not parsed_urls:
        raise ValueError("No valid Telegram post URLs found")

    return parsed_urls
