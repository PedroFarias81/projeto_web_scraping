from telegram import Bot
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def configure_telegram_session() -> Bot:
    """
    Alguma docstring
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    return bot

async def send_telegram_message(bot: Bot, message: str) -> None:
    """
    Alguma docstring
    """
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)