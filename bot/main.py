import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config_bot import bot_settings
from bot.handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=bot_settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())