from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.states import ProcessLLMStates
from services.data import save_input_data, save_output_data
from services.user import get_user_by_tg
from database.database import get_db

# Импортируем сервисы, которые мы уже настроили
from services.embedding_service import EmbeddingService
from services.chroma_service import ChromaService
from services.gpt_service import GPTService
from services.review_query_service import ReviewQueryService
from utils.keyboards import get_common_questions_keyboard
from config import CommonQuestions
from dotenv import load_dotenv
import os


load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_KATALOG_ID = os.getenv("YANDEX_KATALOG_ID")
CHROMA_DB_PATH = "./app/data/chroma_data"

# Инициализация сервисов
embedding_service = EmbeddingService(
    api_key=YANDEX_API_KEY, folder_id=YANDEX_KATALOG_ID
)
chroma_service = ChromaService(collection_name="reviews_collection")
gpt_service = GPTService(api_key=YANDEX_API_KEY, folder_id=YANDEX_KATALOG_ID)

# Сервис для обработки запросов
review_query_service = ReviewQueryService(
    embedding_service, chroma_service, gpt_service
)

router = Router()
session = get_db()


@router.message(ProcessLLMStates.waitForText)
async def request_generate(message: Message, state: FSMContext):
    user_text = message.text
    user = get_user_by_tg(session, message.from_user.id)
    data_id = save_input_data(user.id, user_text, session)

    answer = review_query_service.generate_response_from_gpt(user_text)

    save_output_data(session, answer, data_id, user.id)
    await message.answer(answer)

# Вызывает стандартную клавиатуру под строкой ввода (при замене зафди в utils/keybords.py)
# @router.message(ProcessLLMStates.waitForCommonQuestion)
# async def process_common_question(message: Message, state: FSMContext):
#     if message.text == "Задать свой вопрос":
#         await message.answer("Задайте свой вопрос:")
#         await state.set_state(ProcessLLMStates.waitForText)
#     else:
#         answer = CommonQuestions.QUESTION_ANSWERS.get(message.text)
#         await message.answer(
#             f"Ответ: {answer}",
#             reply_markup=get_common_questions_keyboard(),
#         )
#         await state.set_state(ProcessLLMStates.waitForCommonQuestion)


# Вызывает инлайн клавиатуру в поле чата (при замене зафди в utils/keybords.py)
@router.callback_query(ProcessLLMStates.waitForCommonQuestion)
async def process_common_question(callback_query: CallbackQuery, state: FSMContext):
    selected_question = callback_query.data
    if selected_question == "Задать свой вопрос":
        await callback_query.message.answer("Задайте свой вопрос:")
        await state.set_state(ProcessLLMStates.waitForText)
    else:
        answer = CommonQuestions.QUESTION_ANSWERS.get(selected_question)
        if answer:
            await callback_query.message.answer(
                f"Ответ: {answer}", reply_markup=get_common_questions_keyboard()
            )
        await callback_query.message.delete_reply_markup()
        await state.set_state(ProcessLLMStates.waitForCommonQuestion)
