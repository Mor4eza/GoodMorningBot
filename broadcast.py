import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode

from GoodMorningBot import build_message
from subscribers import load_subscribers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("broadcast")

load_dotenv()


def resolve_recipients() -> list[int]:
    """Subscribers from subscribers.json plus an optional TELEGRAM_CHAT_ID."""
    recipients = load_subscribers()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if chat_id:
        try:
            cid = int(chat_id)
            if cid not in recipients:
                recipients.append(cid)
        except ValueError:
            logger.warning("TELEGRAM_CHAT_ID is not a valid integer, ignoring it")
    return recipients


async def broadcast() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is not set")
        return 0

    recipients = resolve_recipients()
    if not recipients:
        logger.warning("No subscribers found. Nothing to send.")
        return 0

    try:
        message = build_message()
    except Exception as e:
        logger.error(f"Failed to build the daily message: {e}")
        return 0

    sent = failed = 0
    async with Bot(token) as bot:
        for chat_id in recipients:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                sent += 1
                logger.info(f"Sent morning message to {chat_id}")
            except Exception as e:
                failed += 1
                logger.error(f"Failed to send to {chat_id}: {e}")
            await asyncio.sleep(0.05)

    logger.info(f"Broadcast finished: {sent} sent, {failed} failed")
    return sent


if __name__ == "__main__":
    sent = asyncio.run(broadcast())
    if sent == 0:
        sys.exit(1)
