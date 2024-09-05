from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from models.user import User
from models.base import Base


class Data(Base):
    __tablename__ = "data_table"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(User, primaryjoin=user_id == User.id)
    request_date = Column(TIMESTAMP)
    input_data = Column(String)
    output_data = Column(String)
