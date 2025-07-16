import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import router # Import the router from handlers

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    """Configures and starts the bot."""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logging.error("BOT_TOKEN not found in environment variables. Please set it in the .env file.")
        return

    # Initialize bot, storage, and dispatcher
    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Include the router from handlers.py
    dp.include_router(router)

    logging.info("Starting bot...")
    # Start polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
