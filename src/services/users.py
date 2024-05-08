from typing import List
from db.models.users import Users
from schemas.users import UserRequest
from utils.repository import AbstractRepository


class UsersService:
    def __init__(self, user_repo: AbstractRepository) -> None:
        self.users_repo: AbstractRepository = user_repo()

    async def add_user(self, user: UserRequest):
        user_dict = user.model_dump()
        new_user: Users = await self.users_repo.add_one(user_dict)
        new_user.__delattr__('password')
        return new_user
    
    async def get_all(self, limit: int = 10):
        users: List[Users] = await self.users_repo.get_all(limit)
        return users
    
    async def get_one(self, id: int):
        user: Users = await self.users_repo.get_one_by_id(id)
        return user
    

    