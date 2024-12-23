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
from utils.keyboards import inline_keyboards
from utils.texts import SystemMessages
from config import CommonQuestions, GPT_Settings


# Инициализация сервисов
embedding_service = EmbeddingService(
    api_key=GPT_Settings.YANDEX_API_KEY, folder_id=GPT_Settings.YANDEX_KATALOG_ID
)
chroma_service = ChromaService(collection_name="reviews_collection")
gpt_service = GPTService(
    api_key=GPT_Settings.YANDEX_API_KEY, folder_id=GPT_Settings.YANDEX_KATALOG_ID
)

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

    # Получаем выбранную компанию из состояния
    data = await state.get_data()
    company_name = data.get("company_name")
    if not company_name:
        await message.answer(SystemMessages.THERE_IS_NO_COMPANY)
        return

    # Сохраняем данные запроса
    data_id = save_input_data(user.id, user_text, session)

    # Генерируем ответ с учетом выбранной компании
    answer = review_query_service.generate_response_from_gpt(
        user_text, {"company": company_name}
    )

    # Сохраняем ответ
    save_output_data(session, answer, data_id, user.id)
    await message.answer(answer)


# Вызывает инлайн клавиатуру в поле чата
@router.callback_query(ProcessLLMStates.waitForCommonQuestion)
async def process_common_question(callback_query: CallbackQuery, state: FSMContext):
    selected_question = callback_query.data
    if selected_question == "Задать свой вопрос":
        await callback_query.message.answer(SystemMessages.QUESTION_ASKING)
        await state.set_state(ProcessLLMStates.waitForText)
    else:
        answer = CommonQuestions.QUESTION_ANSWERS.get(selected_question)
        if answer:
            await callback_query.message.answer(
                answer, reply_markup=inline_keyboards.common_questions()
            )

        await state.set_state(ProcessLLMStates.waitForCommonQuestion)
