from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime


# Модель для категорий продуктов
class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # parent_category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=True) #на будущее

    # Связь с продуктами
    products = relationship("Product", back_populates="category")