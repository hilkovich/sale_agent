from sqlalchemy.orm import Session
from app.models.review import Review, SentimentEnum
from app.models.topic import Topic
from app.models.product import Product
from app.models.company import Company
from app.models.marketplace import Marketplace


def get_reviews_for_embedding(session):
    """Получение отзывов для векторизации, включая текст и метаданные."""
    reviews = session.query(Review).all()
    review_data = []

    for review in reviews:
        # Собираем нужные данные: текст отзыва, метаданные
        review_text = review.text
        product_name = review.product.name
        product_category = review.product.category.name
        company_name = review.product.company.name
        sentiment = review.sentiment.name if isinstance(review.sentiment,
                                                        SentimentEnum) else review.sentiment  # Преобразование SentimentEnum
        review_date = review.review_date.strftime('%Y-%m-%d')
        topics = ', '.join([topic.name for topic in review.topics])

        # Объединяем текст и метаданные
        combined_text = f"{product_name} | {company_name} | {product_category} | {sentiment} | {review_text} | {review_date} | Topics: {topics}"

        # Формируем структуру для дальнейшей работы
        review_data.append({
            'id': review.id,
            'combined_text': combined_text,
            'metadata': {
                'product': product_name,
                'category': product_category,
                'company': company_name,
                'date': review_date,
                'sentiment': sentiment,
                'topics': topics
            }
        })

    return review_data


def get_or_create(session, model, defaults=None, **kwargs):  #FIXME
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


def add_review(session: Session, review_data: dict):
    """Добавляет отзыв в базу данных."""
    product = get_or_create(session, Product, name=review_data['product_name'])
    company = get_or_create(session, Company, name=review_data['company_name'])
    marketplace = get_or_create(session, Marketplace, name=review_data['marketplace_name'])

    # Создаем новый отзыв
    review = Review(
        text=review_data['review_text'],
        review_date=review_data['review_date'],
        product_id=product.id,
        company_id=company.id,
        marketplace_id=marketplace.id,
        sentiment=review_data['sentiment']
    )

    session.add(review)
    session.commit()

    # Добавляем топики
    for topic_name in review_data['topics']:
        topic = get_or_create(session, Topic, name=topic_name)
        review.topics.append(topic)

    session.commit()


def get_review_by_id(session: Session, review_id: int):
    """Получает отзыв по ID."""
    return session.query(Review).filter_by(id=review_id).first()


def get_all_reviews(session: Session):
    """Возвращает все отзывы."""
    return session.query(Review).all()


def get_reviews_by_company(session: Session, company_name: str):
    """Получает все отзывы по компании."""
    company = session.query(Company).filter_by(name=company_name).first()
    if company:
        return session.query(Review).filter_by(company_id=company.id).all()
    return []


def get_reviews_by_product(session: Session, product_name: str):
    """Получает все отзывы по продукту."""
    product = session.query(Product).filter_by(name=product_name).first()
    if product:
        return session.query(Review).filter_by(product_id=product.id).all()
    return []
