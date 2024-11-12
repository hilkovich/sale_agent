import os


class DB_Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database:{POSTGRES_PORT}/postgres"


class TG_Settings:
    TG_BOT_TOKEN: str = os.getenv("TG_BOT_TOKEN")


class GPT_Settings:
    YANDEX_KATALOG_ID: str = os.getenv("YANDEX_KATALOG_ID")
    YANDEX_API_KEY: str = os.getenv("YANDEX_API_KEY")


class CommonQuestions:
    QUESTION_ANSWERS: dict = {
        "Задать свой вопрос": None,
        "Вопрос 1": "Ответ на вопрос 1",
        "Вопрос 2": "Ответ на вопрос 2",
        "Вопрос 3": "Ответ на вопрос 3",
        "Вопрос 4": "Ответ на вопрос 4",
    }
