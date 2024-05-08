from abc import ABC, abstractmethod

from sqlalchemy import Select, insert, select
from db.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_all():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(statement=stmt)
            await session.commit()
            return res.scalar_one()
    
    async def get_all(self, limit: int = 10):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(statement=stmt)
            return res.scalars().all()[:limit]
        
    async def get_one(self, id: int):
        async with async_session_maker() as session:
            stmt: Select = select(self.model).filter_by(id=id)
            res = await session.execute(statement=stmt)
            return res.scalar()
            