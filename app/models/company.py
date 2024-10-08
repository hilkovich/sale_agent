from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Связь с продуктами
    products = relationship("Product", back_populates="company")
    reviews = relationship("Review", back_populates="company")
