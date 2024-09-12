from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime


# Модель для продуктов
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Внешний ключ на категорию продукта
    product_category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=False)
    category = relationship("ProductCategory", back_populates="products")

    # Внешний ключ на компанию
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company", back_populates="products")

    # Связь с отзывами
    reviews = relationship("Review", back_populates="product")
