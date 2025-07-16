import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import register_handlers
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

def main():
    """Starts the bot."""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logging.error("BOT_TOKEN not found in environment variables.")
        return

    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_handlers(dp)

    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
