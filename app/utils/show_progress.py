"""Progress display utility module for Save Restricted Content Bot.

This module provides utilities for formatting and displaying download
progress information in Telegram messages.
"""

import time

from app.core.logger import log


def human_bytes(size: float) -> str:
    """Convert bytes to human-readable format.

    Converts a byte value to a human-readable string with appropriate
    unit (B, KB, MB, GB, TB).

    Args:
        size (float): Size in bytes.

    Returns:
        str: Human-readable size string (e.g., "5.25 MB").

    Example:
        >>> human_bytes(1024)
        '1.0 KB'
        >>> human_bytes(1048576)
        '1.0 MB'
    """
    if not size:
        return "0 B"

    power = 1024
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]

    while size >= power and n < len(units) - 1:
        size /= power
        n += 1

    return f"{round(size, 2)} {units[n]}"


def time_formatter(seconds: float) -> str:
    """Convert seconds to human-readable time format.

    Converts a number of seconds to a human-readable format like
    "1h 30m 45s" or "5m 30s" or "30s".

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Human-readable time string.

    Example:
        >>> time_formatter(3665)
        '1h 1m 5s'
        >>> time_formatter(330)
        '5m 30s'
        >>> time_formatter(45)
        '45s'
    """
    seconds = int(seconds)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"


def build_progress_bar(percentage: float, length: int = 20) -> str:
    """Build a text-based progress bar.

    Creates a visual progress bar using Unicode block characters.

    Args:
        percentage (float): Percentage completed (0-100).
        length (int): Length of the progress bar. Defaults to 20.

    Returns:
        str: A progress bar string like "[████████░░░░░░░░░░]".

    Example:
        >>> build_progress_bar(50, 20)
        '[██████████░░░░░░░░]'
        >>> build_progress_bar(100, 20)
        '[████████████████████]'
    """
    filled = int(length * percentage // 100)
    empty = length - filled

    return f"[{'█' * filled}{'░' * empty}]"


async def show_progress(
    *,
    bot,
    chat_id: int,
    message_id: int,
    current: int,
    total: int,
    start_time: float,
    prefix: str = "⬇️ Downloading...",
) -> None:
    """Display download progress in a Telegram message.

    Updates a Telegram message with current download progress including
    a progress bar, percentage, speed, and ETA. Handles "message was not
    modified" errors gracefully.

    Args:
        bot: The bot client instance for editing messages.
        chat_id (int): The chat ID where the message is located.
        message_id (int): The message ID to edit.
        current (int): Current bytes downloaded.
        total (int): Total bytes to download.
        start_time (float): Unix timestamp when download started.
        prefix (str): Prefix text for the progress message.
            Defaults to "⬇️ Downloading...".
    """
    diff = time.time() - start_time

    percentage = (current / total) * 100 if total else 0
    speed = current / diff if diff > 0 else 0
    eta = int((total - current) / speed) if speed > 0 else 0

    progress_bar = build_progress_bar(percentage)

    text = (
        f"{prefix}\\n\\n"
        f"{progress_bar} {round(percentage, 2)}%\\n\\n"
        f"📦 Done: {human_bytes(current)}\\n"
        f"📁 Total: {human_bytes(total)}\\n"
        f"🚀 Speed: {human_bytes(speed)}/s\\n"
        f"⏳ ETA: {time_formatter(eta)}"
    )

    try:
        await bot.edit_message(chat_id, message_id, text)
    except Exception as e:
        err = str(e).lower()

        if (
            "message was not modified" in err
            or "content of the message was not modified" in err
        ):
            return

        log.error(f"Progress update failed: {str(e)}", "Progress")
