from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Импортируем сервисы, которые мы уже настроили
from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService
from app.services.gpt_service import GPTService
from app.services.review_query_service import ReviewQueryService

# Инициализация приложения FastAPI
app = FastAPI()

# Загружаем переменные окружения
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


# Модель для запроса от пользователя
class QueryRequest(BaseModel):
    query: str


# Маршрут для обработки запросов от пользователя
@app.get("/ask")
async def ask_user():
    # try:
    # Получаем запрос пользователя
    query = "Какое самое вкусное кофе?"

    # Генерируем ответ с использованием отзывов и GPT
    response = review_query_service.generate_response_from_gpt(query)

    return {"response": response}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


# Маршрут для проверки состояния сервиса
@app.get("/health")
async def health_check():
    return {"status": "ok"}

