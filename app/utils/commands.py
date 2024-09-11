from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="bot", description="Запустить бота"),
        # BotCommand(command="help", description="Как пользоваться ботом"),
        BotCommand(command="call", description="Связаться с менеджером"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
