from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime


# Модель для маркетплейсов
class Marketplace(Base):
    __tablename__ = 'marketplaces'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Связь с отзывами
    reviews = relationship("Review", back_populates="marketplace")
