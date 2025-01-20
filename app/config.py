import os


class DB_Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database:{POSTGRES_PORT}/postgres"
    REVIEWS_DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:{POSTGRES_PORT}/reviews"
    )
    CHROMA_DB_PATH = "/app/data/chroma_data"


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


class DataRoutes:
    XLS_ROUTES: list = [
        "app/artifacts/akbars.xlsx",
        "app/artifacts/deppa.xlsx",
        "app/artifacts/rostics.xlsx",
    ]
    CSV_ROUTES: list = ["app/artifacts/data_s_fixed.csv"]
