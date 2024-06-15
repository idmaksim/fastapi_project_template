from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from db.models.user import User
from schemas.user import UserCreate
from utils.repository import AbstractRepository


class UserService:
    def __init__(self, user_repo: AbstractRepository) -> None:
        self.users_repo: AbstractRepository = user_repo()

    async def add_user(self, user: UserCreate):
        user_dict = user.model_dump()
        try:

            new_user: User = await self.users_repo.add_one(user_dict)
            new_user.__delattr__('password')
            return new_user
        
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail=f"User with data {user} already exists",
            )
    
    async def get_all(self, limit: int = 10):
        users: List[User] = await self.users_repo.get_all(limit)
        return users
    
    async def get_one_by_id(self, id: int):
        user: User = await self.users_repo.get_one_by_id(id)
        return user
    
    async def get_one(self, email: str, password: str):
        user: User = await self.users_repo.get_one_by_data(email=email, password=password)
        return user
    
    async def delete_by_id(self, id: int):
        user: User = await self.users_repo.delete_one_by_id(id)
        return user
    

    