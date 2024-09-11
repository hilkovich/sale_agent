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
    msg = """
    Вас приветствует компания Napoleon IT Отзывы!
    Предлагаем ознакомится с нашим AI инструментом для анализа отзывов.
    Мы поможем вам глубже понять мнения клиентов, предоставляя точные данные. 
    Наша система выявляет тренды в позитивных и негативных отзывах, позволяя быстрее реагировать на изменения в настроениях.
    Система - это централизованный сбор отзывов со всех источников и аналитические исследования. Вы сможете:
    - Изучить выявленные тем и настроения клиентов
    - Попробовать виджет сумаризации отзывов
    - Оценить негативные и позитивные тренды
    - Скачать операционные и стратегические отчеты
    - Провести сравнение с конкурентами
    - Получить систему алертов
    - Воспользоваться генерацией rich контента
    Благодаря этому боту вы можете потрогать все эти данные на своей компании. Аналитика содержит данные за последние 1 000 отзывов.
    """
    await message.answer(msg)
    await cmd_bot(message, state)


@router.message(Command("bot"))
async def cmd_bot(message: Message, state: FSMContext):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    msg = "Задайте свой вопрос или воспользуйтесь меню для консультации с менеджером"
    await message.answer(msg)
    await state.set_state(ProcessLLMStates.waitForText)


# @router.message(Command("help"))
# async def cmd_help(message: Message):
#     user = get_user_by_tg(session, message.from_user.id)
#     if user is None:
#         user_add(session, message.from_user.id)
#     msg = "Раздел помощи с приложением\n" "А это помощь"
#     await message.answer(msg)


@router.message(Command("call"))
async def cmd_call(message: Message):
    user = get_user_by_tg(session, message.from_user.id)
    if user is None:
        user_add(session, message.from_user.id)
    msg = "Для связи с менеджером пройдите по ссылке\n" "[телеграм]"
    await message.answer(msg)
