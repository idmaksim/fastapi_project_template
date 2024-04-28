from db import AbstractBase, engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time


class Users(AbstractBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)
    gender_id: int = Column(Integer, default=1)


class VerificationCodes(AbstractBase):
    __tablename__ = 'verification_codes'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    verification_code: int = Column(Integer, nullable=False)


AbstractBase.metadata.create_all(bind=engine)