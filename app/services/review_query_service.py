from services.chroma_service import ChromaService
from services.gpt_service import GPTService
from services.embedding_service import EmbeddingService
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
import os
from dotenv import load_dotenv


class ReviewQueryService:
    def __init__(self, embedding_service: EmbeddingService, chroma_service: ChromaService, gpt_service: GPTService):
        self.embedding_service = embedding_service
        self.chroma_service = chroma_service
        self.gpt_service = gpt_service

    def search_reviews_in_chroma(self, query: str, n_results: int = 5):
        # Генерируем вектор для запроса
        query_embedding = self.embedding_service.get_query_embedding(query)

        # Выполняем запрос в Chroma
        return self.chroma_service.query_embeddings(query_embedding=query_embedding, n_results=n_results)

    def generate_response_from_gpt(self, query: str) -> str:
        # Ищем отзывы в Chroma
        reviews = self.search_reviews_in_chroma(query)

        # Получаем ответ от GPT на основе найденных отзывов
        gpt_response = self.gpt_service.get_gpt_response(query, reviews)

        return gpt_response


