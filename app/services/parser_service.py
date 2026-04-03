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
