import time

from app.core.logger import log


def human_bytes(size: float) -> str:
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
):
    diff = time.time() - start_time

    percentage = (current / total) * 100 if total else 0
    speed = current / diff if diff > 0 else 0
    eta = int((total - current) / speed) if speed > 0 else 0

    progress_bar = build_progress_bar(percentage)

    text = (
        f"{prefix}\n\n"
        f"{progress_bar} {round(percentage, 2)}%\n\n"
        f"📦 Done: {human_bytes(current)}\n"
        f"📁 Total: {human_bytes(total)}\n"
        f"🚀 Speed: {human_bytes(speed)}/s\n"
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
