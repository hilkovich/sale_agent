import os
import json
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain_core.language_models.llms import LLM

from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document

from YaLLM import YandexLLM
from YaEmbed import YandexEmbeddings
from DocProcess import DocumentProcessor
from EmbedManag import EmbeddingManager

load_dotenv()

api_key = os.getenv('YANDEX_API_KEY')
folder_id = os.getenv('YANDEX_KATALOG_ID')

embeding_model = YandexEmbeddings(api_key, folder_id)
llm_model = YandexLLM(api_key=api_key, folder_id=folder_id)

# Инициализация
api_key = os.getenv('YANDEX_API_KEY')
folder_id = os.getenv('YANDEX_KATALOG_ID')
file_path = os.path.join(os.getcwd(), 'data', 'Tasty_cofee_data.xlsx')

# Обработка документов
doc_processor = DocumentProcessor(embeding_model, file_path)
reviews = doc_processor.load_reviews()

# Генерация эмбеддингов
# doc_embeddings = doc_processor.get_doc_embeddings(reviews)

# Сохранение эмбеддингов
output_file = os.path.join(os.getcwd(), 'data', 'doc_embeddings.json')
# doc_processor.save_embeddings(doc_embeddings, output_file)

# Загрузка эмбеддингов
doc_embeddings = doc_processor.load_embeddings(output_file)

# Проверка эмбенддингов
doc_processor.check_embeddings(doc_embeddings)

embedding_manager = EmbeddingManager()
collection_name = "InternalDocs"
collection = embedding_manager.create_collection(collection_name)
embedding_manager.add_to_collection(collection, doc_embeddings, reviews)

def handle_prompt(query):
    query_embedding = json.loads(doc_processor.embeding_model.embed_query(query))["embedding"]
    relevant_docs = embedding_manager.query_collection(collection, query_embedding, n_results=5)

    # Обработка результатов и вывод
    relevant_docs_lgch = [
        Document(
            page_content=doc, 
            metadata=meta if meta is not None else {}  # Убедитесь, что метаданные не пустые
        ) 
        for doc, meta in zip(relevant_docs['documents'][0], relevant_docs['metadatas'][0])
    ]

    # print("Релевантные документы:")
    # for i, doc in enumerate(relevant_docs_lgch):
    #     print(f"\nДокумент {i+1}:")
    #     print(f"Текст: {doc.page_content}")
    #     print(f"Метаданные: {doc.metadata}")

    document_template = PromptTemplate(
        input_variables=["page_content"], 
        template="{page_content}" 
    )

    document_variable_name = "context"

    template_override = """
        Представь что ты сотрудник компании.
        Пожалуйста, посмотри на текст ниже и ответь на вопрос, используя только информацию из этого текста.
        Текст:
        -----
        {context}
        -----
        Вопрос:
        {query}
    """

    prompt_template = PromptTemplate(
        input_variables=["context", "query"],
        template=template_override
    )

    llm_chain = LLMChain(llm=llm_model, prompt=prompt_template)

    chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_prompt=document_template,
        document_variable_name=document_variable_name
    )

    result = chain.run(input_documents=relevant_docs_lgch, query=query)
    return result
    
print(handle_prompt("Какой кофе лучше?"))