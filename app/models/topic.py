from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime
from app.models.review import review_topic_table


# Модель для тем (топиков) отзывов
class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Связь с отзывами
    reviews = relationship("Review", secondary=review_topic_table, back_populates="topics")
