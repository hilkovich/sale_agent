from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from services.user import user_add, get_user_by_tg
from services.data import save_user_action
from utils.states import ProcessLLMStates
from database.database import get_db
from config import SystemTexts

router = Router()
session = get_db()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    save_user_action(session, "start", user.id)
    msg = SystemTexts.START_MESSAGE
    await message.answer(msg)
    await cmd_bot(message, state)


@router.message(Command("feedback"))
async def reviews_info(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "feedback", user.id)
    msg = SystemTexts.FEEDBACK_MESSAGE
    await message.answer(msg)


@router.message(Command("help"))
async def widget_info(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "help", user.id)
    msg = SystemTexts.START_MESSAGE
    await message.answer(msg)


@router.message(Command("widget"))
async def widget_info(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    save_user_action(session, "widget", user.id)
    msg = SystemTexts.WIDGET_MESSAGE
    await message.answer(msg)


@router.message(Command("chat"))
async def cmd_bot(message: Message, state: FSMContext):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    save_user_action(session, "chat", user.id)
    msg = SystemTexts.CHAT_MESSAGE
    await message.answer(msg)
    await state.set_state(ProcessLLMStates.waitForText)


@router.message(Command("call"))
async def cmd_call(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    save_user_action(session, "call", user.id)
    msg = SystemTexts.CONTACT_MESSAGE
    await message.answer(msg)
