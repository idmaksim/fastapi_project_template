from datetime import datetime

from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String


class Role(Base):
    __tablename__ = 'role'

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: str = Column(String, nullable=False, unique=True) 


class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username: str = Column(String, nullable=False)
    registered_at =  Column(TIMESTAMP, default=datetime.now)
    role_id: int = Column(Integer, ForeignKey('role.id'))
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)    