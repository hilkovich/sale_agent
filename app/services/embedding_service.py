from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from app.services.review_service import get_reviews_for_embedding
from sqlalchemy.orm import Session


class EmbeddingService:
    def __init__(self, api_key: str, folder_id: str):
        """Инициализация сервиса для векторизации с использованием Yandex GPT Embeddings."""
        self.embedding_model = YandexGPTEmbeddings(api_key=api_key, folder_id=folder_id)

    def vectorize_reviews(self, session: Session):
        """Векторизация всех отзывов."""
        reviews = get_reviews_for_embedding(session)
        review_texts = [review['combined_text'] for review in reviews]

        # Векторизация текстов отзывов через Yandex GPT Embeddings
        review_vectors = []
        for text in review_texts:
            try:
                vectors = self.embedding_model.embed_documents([text])
                review_vectors.append(vectors)
            except Exception as e:
                print(f"Ошибка при векторизации: {e}")

        return review_vectors
