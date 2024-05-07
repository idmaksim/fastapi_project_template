from sqlalchemy import Column, Integer, String

from schemas.users import UserRead
from ..db import Base



class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)

    def to_read_model(self) -> UserRead:
        return  UserRead(
            id=self.id,
            email=self.email,
            password=self.password,
            name=self.name
        )