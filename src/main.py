import asyncio
import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.handlers.user_handlers import register_user_handlers


async def main() -> None:
    """Entry point
    """
    logging.info("Starting bot initialization")

    load_dotenv('.env')

    token = os.getenv("TG_API_TOKEN")
    bot = Bot(token = token)
    dp = Dispatcher()

    logging.info("Bot and dispatcher initialized")

    register_user_handlers(dp)

    logging.info("Handlers registered successfully")

    try:
        logging.info("Starting polling")
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"Critical error occurred: {ex}", exc_info=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    asyncio.run(main())