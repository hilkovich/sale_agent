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
    msg = "Добрый день 👋\n" "Что бы Вы хотели узнать про Вашу компанию?"
    await message.answer(msg)
    await state.set_state(ProcessLLMStates.waitForText)
