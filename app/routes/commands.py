from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from services.user import user_add, get_user_by_tg
from utils.states import ProcessLLMStates
from database.database import get_db

router = Router()
session = get_db()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    msg = "Что бы Вы хотели узнать?"
    await message.answer(msg)
    await state.set_state(ProcessLLMStates.waitForText)


@router.message(Command("help"))
async def cmd_help(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    msg = "Раздел помощи с приложением\n" "А это помощь"
    await message.answer(msg)


@router.message(Command("call"))
async def cmd_call(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    msg = "Для связи с менеджером пройдите по ссылке\n" "Ссылка для связи"
    await message.answer(msg)