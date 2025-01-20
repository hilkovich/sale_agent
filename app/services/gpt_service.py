from langchain.chains import LLMChain
from langchain.memory.buffer import ConversationBufferMemory
from langchain_community.llms import YandexGPT
from langchain_core.prompts import PromptTemplate

memory = ConversationBufferMemory(memory_key="chat_history", input_key="query")

class GPTService:
    def __init__(self, api_key: str, folder_id: str):
        # Инициализация Yandex GPT модели
        self.llm = YandexGPT(api_key=api_key, folder_id=folder_id)

    def get_gpt_response(self, query: str, chroma_results: dict) -> str:
        # ToDo: retrieve memory messages here
        """
        Получает ответ от Yandex GPT на основе запроса и найденных отзывов.
        :param query: Вопрос пользователя
        :param reviews: Список релевантных отзывов (с текстом и метаданными)
        :return: Ответ от GPT
        """

        # Извлекаем документы и метаданные
        documents = chroma_results.get("documents", [[]])[
            0
        ]  # Получаем список документов
        metadatas = chroma_results.get("metadatas", [[]])[
            0
        ]  # Получаем список метаданных

        # Проверяем, что есть данные для работы
        if not documents or not metadatas:
            return "Не удалось найти релевантные отзывы для данного запроса."

        # Формируем текст отзывов
        review_texts = "\n".join(
            [
                f"Отзыв: {doc}\nПродукт: {meta['product']}\nКатегория: {meta['category']}\nСентимент: {meta['sentiment']}\nТемы: {meta['topics']}"
                for doc, meta in zip(
                    documents, metadatas
                )  # Соединяем каждый документ с его метаданными
            ]
        )

        # Промпт
        prompt_template = """
        Ты менеджер по продажам в IT компании. 
        Твоя задача — на основе приведённых отзывов сформировать исчерпывающий и точный ответ на вопрос.

        Вот отзывы, которые тебе доступны:
        -----
        {reviews}
        -----
        
        Вот история чата:
        ---
        {chat_history}
        ---
        
        Используя эти отзывы и историю чата, ответь на следующий вопрос максимально полно. 
        Если не знаешь ответа, скажи, что не знаешь.

        Вопрос: {query}
        """

        template = PromptTemplate(
            input_variables=["reviews", "chat_history", "query"], template=prompt_template
        )

        # Создаем цепочку для выполнения запроса в LLM
        llm_chain = LLMChain(prompt=template, llm=self.llm, memory=memory)

        # ToDo here invoke chat history. Current realisation is a simple service-oriented storage.
        # Получаем ответ от GPT
        response = llm_chain.run({"reviews": review_texts, "query": query})

        return response
