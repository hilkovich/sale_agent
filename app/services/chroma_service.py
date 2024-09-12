import chromadb
from typing import List
import os
from chromadb.config import Settings
from chromadb import PersistentClient


class ChromaService:
    def __init__(self, collection_name: str, chroma_db_path: str = "/app/data/chroma_data"):
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
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
