import config
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declared_attr


engine = create_engine(config.SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autoflush=False, bind=engine)


class MyBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    __table_args__ = {
        'extend_existing': True
    }


AbstractBase = declarative_base(cls=MyBase)


def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()
