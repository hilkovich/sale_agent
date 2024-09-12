# class PromptService:
#     def __init__(self, faiss_store, vectorizer_service):
#         self.faiss_store = faiss_store
#         self.vectorizer_service = vectorizer_service
#
#     def augment_prompt(self, user_query):
#         """
#         Дополняет запрос пользователя релевантными отзывами.
#         """
#         # Векторизуем запрос
#         query_vector = self.vectorizer_service.vectorize_text(user_query)
#
#         # Ищем релевантные отзывы
#         relevant_reviews = self.faiss_store.search_vectors(query_vector)
#
#         # Собираем их в текст для дополнения промпта
#         relevant_texts = "\n\n".join([r.text for r in relevant_reviews])
#
#         prompt = f"""
#         Ты отвечаешь на вопросы про продукт. Вот релевантные отзывы:
#
#         {relevant_texts}
#
#         Ответь на вопрос: {user_query}
#         """
#         return prompt
from langchain_core.prompts import PromptTemplate
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain.docstore.document import Document


class PromptService:
    def __init__(self, llm_model):
        self.llm_model = llm_model

    def create_prompt(self, query: str, reviews):
        """Создает промпт для GPT на основе отзывов и метаданных."""
        document_template = PromptTemplate(
            input_variables=["page_content"],
            template="{page_content}"
        )

        document_variable_name = "context"
        template_override = """
            Представь, что ты сотрудник компании.
            Посмотри на текст ниже и ответь на вопрос, используя только информацию из текста.
            Метаданные:
            Продукт: {product}
            Компания: {company}
            Категория: {category}
            Сентимент: {sentiment}
            Дата: {date}
            Топики: {topics}
            -----
            {context}
            -----
            Вопрос:
            {query}
        """

        prompt_template = PromptTemplate(
            input_variables=["context", "query", "product", "company", "category", "sentiment", "date", "topics"],
            template=template_override
        )

        llm_chain = LLMChain(llm=self.llm_model, prompt=prompt_template)

        documents = [
            Document(page_content=review['combined_text'], metadata=review['metadata'])
            for review in reviews
        ]

        chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_template,
            document_variable_name=document_variable_name
        )

        result = chain.run(input_documents=documents, query=query)
        return result
