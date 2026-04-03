import re


def is_valid_telegram_post_url(url: str) -> bool:
    pattern = r"^https:\/\/t\.me\/c\/\d+\/\d+$"
    return bool(re.match(pattern, url.strip()))
