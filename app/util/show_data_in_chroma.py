import chromadb
from app.services.chroma_service import ChromaService





# Инициализация клиента Chroma
# client = chromadb.Client()
# # Получаем список всех коллекций
# collections = client.list_collections()
# print("Доступные коллекции:")
# for collection in collections:
#     print(collection.name)

# Получаем коллекцию, с которой хотим работать
# collection = client.get_collection("reviews_collection")

# # Получаем все документы из коллекции
# all_documents = collection.get()
# print("\nДокументы в коллекции 'reviews_collection':")
# for i, doc in enumerate(all_documents['documents']):
#     print(f"Документ {i + 1}:")
#     print(f"Текст: {doc}")
#     print(f"Метаданные: {all_documents['metadatas'][i]}")


# Инициализация Chroma сервиса
chroma_service = ChromaService(collection_name="reviews_collection")


def check_collection(n_results=3):
    """Проверка, создалась ли коллекция и записаны ли эмбеддинги."""
    try:
        # Получаем коллекцию
        collection = chroma_service.get_or_create_collection()

        # Проверяем количество записей в коллекции
        embeddings_count = collection.count()
        print(f"Количество эмбеддингов в коллекции 'reviews_collection': {embeddings_count}")

        if embeddings_count > 0:
            # Создаём фиктивный запрос, чтобы получить любые первые результаты
            fake_query_embedding = [0] * 256

            # Получаем первые n_results эмбеддингов на основе фиктивного запроса
            results = collection.query(
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
        else:
            print("Коллекция пуста.")

    except Exception as e:
        print(f"Ошибка при проверке коллекции: {e}")


if __name__ == "__main__":
    check_collection(21)
