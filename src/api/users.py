from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder

from repositories.users import UsersRepository
from schemas.users import UserRequest


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserRequest,
):
    user_dict = user.model_dump()
    new_user = await UsersRepository().add_one(user_dict)
    return new_user 

