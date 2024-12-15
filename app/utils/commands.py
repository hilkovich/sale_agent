from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Повторный запуск бота"),
        BotCommand(command="help", description="Как пользоваться ботом"),
        BotCommand(command="feedback", description="Узнать о продукте Отзывы"),
        BotCommand(command="widget", description="Узнать о продукте Виджет"),
        BotCommand(command="chat", description="Задать вопрос помощнику"),
        BotCommand(command="call", description="Связаться с менеджером"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
