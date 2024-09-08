from sqlalchemy import Column, Integer, String
from models.base import Base


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    company_name = Column(String)
    tg_id = Column(Integer)
