import chromadb
from typing import List
import os
from chromadb.config import Settings
from chromadb import PersistentClient


class ChromaService:
    def __init__(self, collection_name: str, chroma_db_path: str = "/app/data/chroma_data"): #FixMe
        """Инициализация Chroma клиента с персистентностью"""
        settings = Settings(persist_directory=chroma_db_path, is_persistent=True)
        self.client = PersistentClient(path=chroma_db_path, settings=settings)
        self.collection_name = collection_name
        self.collection = self.get_or_create_collection()

    def get_or_create_collection(self):
        """Получает или создает коллекцию."""
        collections = self.client.list_collections()
        if self.collection_name in [col.name for col in collections]:
            return self.client.get_collection(self.collection_name)
        else:
            return self.client.create_collection(name=self.collection_name)

    def add_embeddings(self, embeddings: List[List[float]], documents: List[str], metadata: List[dict], ids: List[str] = None):
        """Добавление эмбеддингов в коллекцию Chroma."""
        if ids is None:
            ids = [f"id_{i}" for i in range(len(documents))]

        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata,
            ids=ids
        )
        print(f"Добавлено {len(embeddings)} эмбеддингов в коллекцию {self.collection.name}")

    def query_embeddings(self, query_embedding: List[float], n_results: int = 5):
        """Поиск похожих эмбеддингов в Chroma."""

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "embeddings", "metadatas", "distances"]
        )

        return results

    def check_collection(self, n_results=3):
        """Проверка, создалась ли коллекция и записаны ли эмбеддинги."""
        try:

            # Проверяем количество записей в коллекции
            embeddings_count = self.collection.count()
            print(f"Количество эмбеддингов в коллекции 'reviews_collection': {embeddings_count}")

            if embeddings_count > 0:
                # Создаём фиктивный запрос, чтобы получить любые первые результаты
                fake_query_embedding = [0] * 256

                # Получаем первые n_results эмбеддингов на основе фиктивного запроса
                results = self.collection.query(
                    query_embeddings=[fake_query_embedding],
                    n_results=n_results,
                    include=["documents", "embeddings", "metadatas", "distances"]
                )

                # Проверяем, что результат содержит данные
                if results and 'documents' in results and len(results['documents']) > 0:
                    print("Первые эмбеддинги в коллекции:")
                    for i in range(len(results['documents'])):
                        print(
                            f"Эмбеддинг {i + 1}:\nДокумент: {results['documents'][i]}\nМетаданные: {results['metadatas'][i]}\nЭмбеддинг: {results['embeddings'][i]}\n"
                        )
                else:
                    print("Не удалось получить результаты из коллекции.")

                return results

            else:
                print("Коллекция пуста.")

        except Exception as e:
            print(f"Ошибка при проверке коллекции: {e}")