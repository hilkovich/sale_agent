from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from utils.texts import CommandsTexts


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description=CommandsTexts.START),
        BotCommand(command="help", description=CommandsTexts.HELP),
        BotCommand(command="feedback", description=CommandsTexts.FEEDBACK),
        BotCommand(command="widget", description=CommandsTexts.WIDGET),
        BotCommand(command="chat", description=CommandsTexts.CHAT),
        BotCommand(command="call", description=CommandsTexts.CALL),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
