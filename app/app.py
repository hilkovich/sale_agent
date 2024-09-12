import asyncio
from aiogram import Bot, Dispatcher
from config import TG_Settings
from loguru import logger

from utils.commands import set_commands
from routes import ml, commands

token = TG_Settings.TG_BOT_TOKEN

bot = Bot(token=token)
dp = Dispatcher()


async def start():
    try:
        logger.info("DB initialize completed")
        await set_commands(bot)
        logger.info("bot commands set")
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        logger.info("bot stopped")


dp.include_router(commands.router)
dp.include_router(ml.router)


if __name__ == "__main__":
    asyncio.run(start())
