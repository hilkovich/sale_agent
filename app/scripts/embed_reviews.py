from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from services.review_service import get_reviews_for_embedding
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.chroma_service import ChromaService
from config import GPT_Settings, DB_Settings

# Настройка подключения к базе данных
engine = create_engine(DB_Settings.REVIEWS_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Инициализация модели Yandex Embeddings
embedding_model = YandexGPTEmbeddings(
    api_key=GPT_Settings.YANDEX_API_KEY, folder_id=GPT_Settings.YANDEX_KATALOG_ID
)

# Инициализация Chroma сервиса
chroma_service = ChromaService(collection_name="reviews_collection")


def flatten_embedding(embedding):
    """Преобразует вложенные списки в одномерный список."""
    return [item for sublist in embedding for item in sublist]


def vectorize_reviews(session, n_results=3):
    """Векторизация всех отзывов и сохранение в файл."""

    # Получаем отзывы для векторизации
    reviews = get_reviews_for_embedding(session)
    review_texts = [review["combined_text"] for review in reviews]
    metadata = [review["metadata"] for review in reviews]
    review_ids = [str(review["id"]) for review in reviews]

    # Векторизуем тексты отзывов через API Yandex
    review_vectors = [
        flatten_embedding(embedding_model.embed_documents([text]))
        for text in review_texts
    ]

    # Присваиваем эмбеддингам соответствующие метаданные
    embeddings_data = [
        {
            "id": review_ids[i],
            "embedding": review_vectors[i],
            "document": review_texts[i],
            "metadata": metadata[i],  # Метаданные для каждого эмбеддинга
        }
        for i in range(len(review_texts))
    ]

    # Добавляем эмбеддинги и метаданные в Chroma
    chroma_service.add_embeddings(
        embeddings=[data["embedding"] for data in embeddings_data],
        documents=[data["document"] for data in embeddings_data],
        metadata=[data["metadata"] for data in embeddings_data],
        ids=review_ids,
    )

    print(f"Векторизация завершена. Векторы сохранены в chroma.")


if __name__ == "__main__":
    # Запуск векторизации
    vectorize_reviews(session, 21)
