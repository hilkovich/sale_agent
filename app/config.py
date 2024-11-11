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


class SystemTexts:
    START_MESSAGE: str = """
    Вас приветствует компания Napoleon IT Отзывы!
    Предлагаем ознакомится с нашим AI инструментом для анализа отзывов.
    Мы поможем вам глубже понять мнения клиентов, предоставляя точные данные. 
    Наша система выявляет тренды в позитивных и негативных отзывах, позволяя быстрее реагировать на изменения в настроениях.
    Система - это централизованный сбор отзывов со всех источников и аналитические исследования. Вы сможете:
    - Изучить выявленные тем и настроения клиентов
    - Попробовать виджет сумаризации отзывов
    - Оценить негативные и позитивные тренды
    - Скачать операционные и стратегические отчеты
    - Провести сравнение с конкурентами
    - Получить систему алертов
    - Воспользоваться генерацией rich контента
    Благодаря этому боту вы можете потрогать все эти данные на своей компании. Аналитика содержит данные за последние 1 000 отзывов.
    """
    FEEDBACK_MESSAGE: str = "У нас есть отзывы! Много отзывов!"
    WIDGET_MESSAGE: str = "Виджет - это круто! Покупай виджет!"
    CHAT_MESSAGE: str = "Задайте свой вопрос или воспользуйтесь меню для перехода в другой раздел"
    CONTACT_MESSAGE: str = "Для связи с менеджером пройдите по ссылке\n" "[телеграм]"
