import asyncio

from app.core.bot import run_bot

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\nBot stopped manually.")
