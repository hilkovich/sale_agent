from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from models.user import User
from models.base import Base


class Data(Base):
    __tablename__ = "data_table"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(User, primaryjoin=user_id == User.id)
    request_date = Column(TIMESTAMP)
    input_data = Column(JSONB)
    output_data = Column(JSONB)


class Action(Base):
    __tablename__ = "user_actions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(User, primaryjoin=user_id == User.id)
    action_date = Column(TIMESTAMP)
    action_type = Column(String)