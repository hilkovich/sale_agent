from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from models.base import Base
from models.user import User


class Reviews(Base):
    __tablename__ = "reviews_table"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(User, primaryjoin=user_id == User.id)
    product_category = Column(String)
    product_name = Column(String)
    review_date = Column(TIMESTAMP)
    review_text = Column(String)
    topic = Column(String)
    sentiment = Column(String)
    marketplace = Column(String)
    username = Column(String, ForeignKey("user_table.company_name"))
    company = relationship(User, primaryjoin=username == User.company_name)
