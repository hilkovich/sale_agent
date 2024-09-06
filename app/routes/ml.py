from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.states import ProcessLLMStates
from services.ml import response
from services.data import save_input_data, save_output_data
from database.database import get_db

router = Router()
session = get_db()


@router.message(ProcessLLMStates.waitForText)
async def cmn_create_book(message: Message, state: FSMContext):
    user_text = message.text
    tg_id = message.from_user.id

    data_id = save_input_data(tg_id, user_text, session)
    answer = response(
        data=user_text
    )  # в функции response() прописать обращение к модели для генерации ответа

    save_output_data(session, answer, data_id, tg_id)
    await message.answer(answer)
    await state.clear()
