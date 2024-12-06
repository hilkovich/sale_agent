import os
import logging
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from pymilvus import (
    connections,
    utility,
    DataType,
    FieldSchema,
    Collection,
    CollectionSchema,
)
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_milvus.utils.sparse import BM25SparseEmbedding

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def connect_to_milvus(host="localhost", port="19530"):
    logger.info(f"Подключение к Milvus на {host}:{port}...")
    connections.connect(host=host, port=port)
    version = utility.get_server_version()
    logger.info(f"Версия сервера Milvus: {version}")


def generate_embeddings(df, text_column="Описание"):
    logger.info(f"Генерация эмбеддингов для столбца '{text_column}'...")
    dense_embeddings = HuggingFaceBgeEmbeddings(
        model_name="deepvk/USER-bge-m3"
    ).embed_documents(df[text_column].fillna("").tolist())
    sparse_embeddings = BM25SparseEmbedding(
        corpus=df[text_column].fillna("").tolist()
    ).embed_documents(df[text_column].fillna("").tolist())
    logger.info(
        f"Сгенерировано {len(dense_embeddings)} плотных эмбеддингов и {len(sparse_embeddings)} разреженных эмбеддингов."
    )
    return dense_embeddings, sparse_embeddings


def process_sparse_embeddings(sparse_embeddings, target_dim=1000):
    sparse_embeddings_fixed = []
    logger.info("Обработка разреженных эмбеддингов...")
    for embedding in sparse_embeddings:
        vector = np.zeros(target_dim, dtype=np.float32)
        for idx, value in embedding.items():
            if 0 <= int(idx) < target_dim:
                vector[int(idx)] = value
        sparse_embeddings_fixed.append(vector)
    logger.info(f"Обработано {len(sparse_embeddings_fixed)} разреженных эмбеддингов.")
    return sparse_embeddings_fixed


def create_collection_schema(target_dim=1000):
    logger.info(f"Создание схемы коллекции с размерностью эмбеддингов: {target_dim}...")
    id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True)
    dense_embedding_field = FieldSchema(
        name="dense_embedding", dtype=DataType.FLOAT_VECTOR, dim=target_dim
    )
    sparse_embedding_field = FieldSchema(
        name="sparce_embedding", dtype=DataType.FLOAT_VECTOR, dim=target_dim
    )
    title_field = FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500)
    link_field = FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=500)

    schema = CollectionSchema(
        fields=[
            id_field,
            dense_embedding_field,
            sparse_embedding_field,
            title_field,
            link_field,
        ],
        description="Collection with documents",
    )
    return schema


def create_or_get_collection(collection_name="hybrid_search_documents", schema=None):
    logger.info(f"Создание или получение коллекции '{collection_name}'...")
    try:
        collection = Collection(name=collection_name, schema=schema)
        logger.info(f"Коллекция '{collection_name}' найдена.")
    except Exception as e:
        logger.info(f"Коллекция '{collection_name}' не найдена. Создание новой...")
        collection = Collection(name=collection_name, schema=schema)
    return collection


def insert_data_to_collection(
    collection, df, dense_embeddings, sparse_embeddings_fixed
):
    logger.info(f"Вставка данных в коллекцию...")
    data = [
        list(range(len(df))),
        dense_embeddings,
        sparse_embeddings_fixed,
        df["Заголовок"].fillna("").tolist(),
        df["Ссылка"].fillna("").tolist(),
    ]
    collection.insert(data)
    logger.info(f"Успешно вставлено {len(data[0])} документов в коллекцию.")


def create_index(collection, target_dim=1000):
    # Индекс для плотных эмбеддингов (HNSW)
    indexes = collection.indexes
    dense_index_exists = False
    for index in indexes:
        if index.field_name == "dense_embedding":
            dense_index_exists = True
            break

    if not dense_index_exists:
        index_params_dense = {
            "metric_type": "L2",
            "index_type": "HNSW",
            "params": {"M": 16, "efConstruction": 200},
        }
        collection.create_index(
            field_name="dense_embedding", index_params=index_params_dense
        )
        logger.info("Индекс для плотных эмбеддингов создан.")
    else:
        logger.info("Индекс для плотных эмбеддингов уже существует.")

    # Индекс для разреженных эмбеддингов (IVF_FLAT)
    sparse_index_exists = False
    for index in indexes:
        if index.field_name == "sparce_embedding":
            sparse_index_exists = True
            break

    if not sparse_index_exists:
        index_params_sparse = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024},
        }
        collection.create_index(
            field_name="sparce_embedding", index_params=index_params_sparse
        )
        logger.info("Индекс для разреженных эмбеддингов создан.")
    else:
        logger.info("Индекс для разреженных эмбеддингов уже существует.")


def search_in_collection(collection, query_embeddings, top_k=5):
    logger.info(f"Поиск в коллекции по запросу...")
    collection.load()

    search_params = {"metric_type": "L2", "params": {"ef": 64}}

    output_fields = ["title"]
    results = collection.search(
        query_embeddings,
        "dense_embedding",
        search_params,
        top_k,
        output_fields=output_fields,
    )

    logger.info(f"Результаты поиска: {results}")
    return results


# TODO: добавить гибридный поиск


def main(file_path="data/news_Пермь.xlsx", query = "Что произошло в Перми?", target_dim=1000):
    connect_to_milvus()

    df = pd.read_excel(file_path)
    dense_embeddings, sparse_embeddings = generate_embeddings(df)

    dense_embeddings = [embedding[:target_dim] for embedding in dense_embeddings]
    sparse_embeddings_fixed = process_sparse_embeddings(sparse_embeddings, target_dim)

    schema = create_collection_schema(target_dim)
    collection = create_or_get_collection(
        collection_name="hybrid_search_documents", schema=schema
    )

    insert_data_to_collection(collection, df, dense_embeddings, sparse_embeddings_fixed)

    create_index(collection, target_dim)

    query_embedding = HuggingFaceBgeEmbeddings(
        model_name="deepvk/USER-bge-m3"
    ).embed_documents([query])[0][:target_dim]

    print(search_in_collection(collection, [query_embedding], top_k=5))

if __name__ == "__main__":
    main()