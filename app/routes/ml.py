from aiogram import Router
from aiogram.types import Message
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
from dotenv import load_dotenv
import os


load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_KATALOG_ID = os.getenv("YANDEX_KATALOG_ID")
CHROMA_DB_PATH = "./app/data/chroma_data"

# Инициализация сервисов
embedding_service = EmbeddingService(api_key=YANDEX_API_KEY, folder_id=YANDEX_KATALOG_ID)
chroma_service = ChromaService(collection_name="reviews_collection")
gpt_service = GPTService(api_key=YANDEX_API_KEY, folder_id=YANDEX_KATALOG_ID)

# Сервис для обработки запросов
review_query_service = ReviewQueryService(embedding_service, chroma_service, gpt_service)

router = Router()
session = get_db()


@router.message(ProcessLLMStates.waitForText)
async def request_generate(message: Message, state: FSMContext):
    user_text = message.text
    tg_id = message.from_user.id
    user = get_user_by_tg(session, tg_id)
    data_id = save_input_data(user.id, user_text, session)

    answer = review_query_service.generate_response_from_gpt(user_text)

    save_output_data(session, answer, data_id, user.id)
    await message.answer(answer)
