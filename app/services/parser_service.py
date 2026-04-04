import re


def parse_telegram_post_url(url: str) -> tuple[int, int]:
    """
    Parses Telegram private channel post URLs like:
    https://t.me/c/3776460651/4

    Returns:
        (channel_id, message_id)
        e.g. (-1003776460651, 4)
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
    """
    Parses multiple Telegram post URLs from multiline input.

    Example input:
        https://t.me/c/3776460651/20
        https://t.me/c/3776460651/21
        https://t.me/c/3776460651/22

    Returns:
        list of tuples:
        [
            (channel_id, message_id, original_url),
            ...
        ]

    Example:
        [
            (-1003776460651, 20, "https://t.me/c/3776460651/20"),
            (-1003776460651, 21, "https://t.me/c/3776460651/21"),
        ]
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
