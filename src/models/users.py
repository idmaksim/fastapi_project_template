from sqlalchemy import Column, Integer, String
from ..db.db import Base
from ..schemas.users import UserRead


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