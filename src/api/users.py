from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import users_service
from schemas.users import UserRequest
from services.users import UsersService
from utils.error_handler import handle_route_error


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserRequest,
    user_service: Annotated[UsersService, Depends(users_service)]
):
    try:
        new_user = await user_service.add_user(user)
        return new_user
    
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/all')
async def get_all_users(
    user_service: Annotated[UsersService, Depends(users_service)]
):
    try:
        users = await user_service.get_all()
        if users:
            return users
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='users not found'
        )
        
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

