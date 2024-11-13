from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Повторный запуск бота"),
        BotCommand(command="help", description="Посмотреть как пользоваться ботом"),
        BotCommand(
            command="feedback", description="Узнать о продукте NapoleonIT-отзывы"
        ),
        BotCommand(command="widget", description="Узнать о виджете для вашего сайта"),
        BotCommand(command="chat", description="Задать вопрос боту"),
        BotCommand(command="call", description="Связаться с менеджером"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
