from app.core.logger import log


async def update_batch_log(
    *,
    bot,
    chat_id: int,
    message_id: int,
    entries: list[str],
):
    if not entries:
        text = "Downloaded Posts:\n\n⏳ No completed downloads yet..."
    else:
        text = "Downloaded Posts:\n\n" + "\n\n".join(entries)

    try:
        await bot.edit_message(chat_id, message_id, text)
    except Exception as e:
        err = str(e).lower()

        if (
            "message was not modified" in err
            or "content of the message was not modified" in err
        ):
            return

        log.error(f"Batch log update failed: {str(e)}", "BatchLog")
