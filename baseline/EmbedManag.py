import chromadb

class EmbeddingManager:
    def __init__(self):
        self.client = chromadb.Client()
    
    def create_collection(self, collection_name):
        collections = self.client.list_collections()
        if collection_name in [col.name for col in collections]:
            self.client.delete_collection(collection_name)
        return self.client.get_or_create_collection(name=collection_name)

    def add_to_collection(self, collection, embeddings, documents):
        collection.add(
            embeddings=embeddings,
            documents=documents,
            ids=[f"id_{i}" for i in range(len(documents))]
        )
        print(f"Добавлено {len(embeddings)} эмбеддингов в коллекцию {collection.name}")

    def query_collection(self, collection, query_embedding, n_results=5):
        return collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )