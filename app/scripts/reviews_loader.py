from app.models import Product, ProductCategory,Review, Topic, Company, Marketplace, review_topic_table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv


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
def load_reviews_from_csv(csv_file):
    engine = create_engine("postgresql://postgres:postgres@db:5432/reviews")
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        # Выводим заголовки CSV-файла
        print("Headers:", reader.fieldnames)

        for row in reader:
            # Проверка и создание компании
            company = get_or_create(session, Company, name=row['Username'])

            # Проверка и создание маркетплейса
            marketplace = get_or_create(session, Marketplace, name=row['Marketplace'])

            product_category = get_or_create(session, ProductCategory, name=row['Product Category'])

            # Проверка и создание продукта
            product = get_or_create(
                session,
                Product,
                name=row['Product Name'],
                product_category_id=product_category.id,
                company_id=company.id
            )

            # Создание отзыва
            review = Review(
                text=row['Review'],
                review_date=row['Review Date'],
                product_id=product.id,
                sentiment=row['Sentiment'],
                marketplace_id=marketplace.id,
                company_id=company.id
            )
            session.add(review)
            session.commit()

            # Работа с топиками
            topics = row['Topic_r'].split(', ')
            for topic_name in topics:
                topic = get_or_create(session, Topic, name=topic_name)
                # Добавляем топик к отзыву через промежуточную таблицу
                session.execute(review_topic_table.insert().values(review_id=review.id, topic_id=topic.id))

            session.commit()

    session.close()


# Пример использования
csv_file_path = './data/data_s_fixed.csv'
load_reviews_from_csv(csv_file_path)
