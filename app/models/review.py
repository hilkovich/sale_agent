from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, Enum
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime
import enum


# Определение возможных значений настроения (Sentiment)
class SentimentEnum(enum.Enum):
    Positive = "Positive"
    Negative = "Negative"
    Neutral = "Neutral"


# Промежуточная таблица для связи отзывов и топиков
review_topic_table = Table('review_topics', Base.metadata,
                           Column('review_id', Integer, ForeignKey('reviews.id'), primary_key=True),
                           Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=True)
                           )


# Модель для отзывов
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    review_date = Column(DateTime, default=datetime.utcnow)

    # Внешний ключ на продукт
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship("Product", back_populates="reviews")

    # Поле для настроения отзыва
    sentiment = Column(Enum(SentimentEnum), nullable=False)

    # Внешний ключ на маркетплейс
    marketplace_id = Column(Integer, ForeignKey('marketplaces.id'), nullable=False)
    marketplace = relationship("Marketplace", back_populates="reviews")

    # Внешний ключ на компанию
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company", back_populates="reviews")


    # # Связь с промежуточной таблицей для тем (топиков)
    topics = relationship("Topic", secondary=review_topic_table, back_populates="reviews")
