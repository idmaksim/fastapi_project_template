from sqlalchemy import Column, Integer, String
from ..db.db import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)