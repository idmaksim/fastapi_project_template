from db import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    __table_args__ = dict(
        extend_existing=True
    )

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)
    age: int = Column(Integer, nullable=False)
    role_id: int = Column(ForeignKey('roles.id'), nullable=False)


class VerificationCodes(Base):
    __tablename__ = 'verification_codes'

    __table_args__ = dict(
        extend_existing=True
    )
    id: int = Column(Integer, primary_key=True, unique=True)
    email: str = Column(String, unique=True, nullable=False)
    verification_code: int = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)
