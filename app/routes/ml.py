from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.states import ProcessLLMStates
from services.ml import response
from services.data import save_input_data, save_output_data
from services.user import get_user_by_tg
from database.database import get_db

router = Router()
session = get_db()


@router.message(ProcessLLMStates.waitForText)
async def request_generate(message: Message, state: FSMContext):
    user_text = message.text
    tg_id = message.from_user.id
    user = get_user_by_tg(session, tg_id)
    data_id = save_input_data(user.id, user_text, session)
    answer = response(data=user_text)

    save_output_data(session, answer, data_id, user.id)
    await message.answer(answer)
