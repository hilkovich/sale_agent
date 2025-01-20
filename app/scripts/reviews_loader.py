from models import (
    Product,
    ProductCategory,
    Review,
    Topic,
    Company,
    Marketplace,
    review_topic_table,
)
from config import DataRoutes, DB_Settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv
import pandas as pd


# Функция для создания или получения объекта
def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.items())
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance


# Функция для загрузки CSV
def load_reviews_from_csv(csv_file: str):
    engine = create_engine(DB_Settings.REVIEWS_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        # Выводим заголовки CSV-файла
        print("Headers:", reader.fieldnames)

        for row in reader:
            # Проверка и создание компании
            company = get_or_create(session, Company, name=row["Username"])

            # Проверка и создание маркетплейса
            marketplace = get_or_create(session, Marketplace, name=row["Marketplace"])

            product_category = get_or_create(
                session, ProductCategory, name=row["Product Category"]
            )

            # Проверка и создание продукта
            product = get_or_create(
                session,
                Product,
                name=row["Product Name"],
                product_category_id=product_category.id,
                company_id=company.id,
            )

            # Создание отзыва
            review = Review(
                text=row["Review"],
                review_date=row["Review Date"],
                product_id=product.id,
                sentiment=row["Sentiment"],
                marketplace_id=marketplace.id,
                company_id=company.id,
            )
            session.add(review)
            session.commit()

            # Работа с топиками
            topics = row["Topic_r"].split(", ")
            for topic_name in topics:
                topic = get_or_create(session, Topic, name=topic_name)
                # Добавляем топик к отзыву через промежуточную таблицу
                session.execute(
                    review_topic_table.insert().values(
                        review_id=review.id, topic_id=topic.id
                    )
                )

            session.commit()

    session.close()


# Функция для загрузки данных из Excel
def load_reviews_from_excel(file_path: str):
    engine = create_engine("postgresql://postgres:postgres@db:5432/reviews")
    Session = sessionmaker(bind=engine)
    session = Session()

    # достаем наименование компании из пути
    company_name = file_path.split("/")[-1].split(".")[0]

    # Читаем Excel файл
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        # Проверка и создание компании
        company = get_or_create(session, Company, name=company_name)

        # Проверка и создание маркетплейса
        marketplace = get_or_create(session, Marketplace, name=row["Источник"])

        # Проверка и создание категории продукта (если столбец "Категория" имеется)
        product_category = get_or_create(
            session, ProductCategory, name=row.get("Категория", "Без категории")
        )

        # Определение сентимента по первому попавшемуся значению в топиках
        sentiment = None
        for col in df.columns[6:]:
            if not pd.isna(row[col]):  # Проверяем наличие значения
                if col.lower() == "Позитивное":
                    sentiment = "Positive"
                elif col.lower() == "Негативное":
                    sentiment = "Negative"
                elif col.lower() == "Нейтральное":
                    sentiment = "Neutral"
                break

        # Если сентимент так и не найден, можно задать значение по умолчанию
        if sentiment is None:
            sentiment = "Neutral"

        # Проверка и создание продукта
        product = get_or_create(
            session,
            Product,
            name=row["Продукт"],
            product_category_id=product_category.id,
            company_id=company.id,
        )

        # Создание отзыва
        review = Review(
            text=row["Текст"],
            review_date=row["Дата публикации"],
            sentiment=sentiment,
            product_id=product.id,
            marketplace_id=marketplace.id,
            company_id=company.id,
        )
        session.add(review)
        session.commit()

        # Работа с топиками
        for column in df.columns[df.columns.get_loc("Дата публикации") + 1 :]:
            topic_value = row[
                column
            ]  # Значение топика (например, "негативное", "позитивное")
            if pd.notna(topic_value):  # Если значение существует
                topic = get_or_create(
                    session, Topic, name=column
                )  # Создаём топик, если его нет
                # Добавляем топик к отзыву через промежуточную таблицу
                session.execute(
                    review_topic_table.insert().values(
                        review_id=review.id, topic_id=topic.id
                    )
                )

        session.commit()

    session.close()


# Загрусзка CSV
if DataRoutes.CSV_ROUTES:
    for csv_file_path in DataRoutes.CSV_ROUTES:
        load_reviews_from_csv(csv_file_path)


# Загрузка Excel
if DataRoutes.XLS_ROUTES:
    for xls_file_path in DataRoutes.XLS_ROUTES:
        load_reviews_from_excel(xls_file_path)
