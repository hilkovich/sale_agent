from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from models.base import Base
from models.user import User


class Analytics(Base):
    __tablename__ = "analytics_table"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(User, primaryjoin=user_id == User.id)
    company_name = Column(String)
