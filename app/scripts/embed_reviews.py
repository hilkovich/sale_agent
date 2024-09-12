import os
import json
from dotenv import load_dotenv
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from services.review_service import get_reviews_for_embedding
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.chroma_service import ChromaService

# Загрузка переменных окружения
load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_KATALOG_ID = os.getenv("YANDEX_KATALOG_ID")

# Настройка подключения к базе данных
DATABASE_URL = "postgresql://postgres:postgres@db:5432/reviews"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Инициализация модели Yandex Embeddings
embedding_model = YandexGPTEmbeddings(api_key=YANDEX_API_KEY, folder_id=YANDEX_KATALOG_ID)

# Инициализация Chroma сервиса
chroma_service = ChromaService(collection_name="reviews_collection")


def flatten_embedding(embedding):
    """Преобразует вложенные списки в одномерный список."""
    return [item for sublist in embedding for item in sublist]


def vectorize_reviews(session, n_results=3):
    """Векторизация всех отзывов и сохранение в файл."""

    # Получаем отзывы для векторизации
    reviews = get_reviews_for_embedding(session)
    review_texts = [review['combined_text'] for review in reviews]
    metadata = [review['metadata'] for review in reviews]
    review_ids = [str(review['id']) for review in reviews]

    # Векторизуем тексты отзывов через API Yandex
    review_vectors = [flatten_embedding(embedding_model.embed_documents([text])) for text in review_texts]

    # Присваиваем эмбеддингам соответствующие метаданные
    embeddings_data = [{
        "id": review_ids[i],
        "embedding": review_vectors[i],
        "document": review_texts[i],
        "metadata": metadata[i]  # Метаданные для каждого эмбеддинга
    } for i in range(len(review_texts))]

    # Добавляем эмбеддинги и метаданные в Chroma
    chroma_service.add_embeddings(
        embeddings=[data["embedding"] for data in embeddings_data],
        documents=[data["document"] for data in embeddings_data],
        metadata=[data["metadata"] for data in embeddings_data],
        ids=review_ids
    )

    print(f"Векторизация завершена. Векторы сохранены в chroma.")


if __name__ == "__main__":
    # Запуск векторизации
    vectorize_reviews(session, 21)
