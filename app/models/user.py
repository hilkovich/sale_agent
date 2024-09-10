from sqlalchemy import Column, BigInteger, Integer, TIMESTAMP
from models.base import Base


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    created_on = Column(TIMESTAMP)
