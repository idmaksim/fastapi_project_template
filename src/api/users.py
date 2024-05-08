from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import users_service
from schemas.users import UserAddRequest
from services.users import UsersService
from utils.error_handler import handle_route_error


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserAddRequest,
    user_service: Annotated[UsersService, Depends(users_service)]
):
    try:
        new_user = await user_service.add_user(user)
        return new_user
    
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_service: Annotated[UsersService, Depends(users_service)],
    id: int
):
    try:
        user = await user_service.get_one_by_id(id)
        if user:
            return user
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
        
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@router.get('', status_code=status.HTTP_200_OK)
async def get_user(
    user_service: Annotated[UsersService, Depends(users_service)],
    email: str,
    password: str
):
    try:
        user = await user_service.get_one(email=email, password=password)
        if user:
            return user
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
        
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_user_by_id(
    user_service: Annotated[UsersService, Depends(users_service)],
    id: int
):
    try:
        user = await user_service.get_one_by_id(id)
        
        if user:
            deleted_user = await user_service.delete_by_id(id)
            return deleted_user
        
        raise HTTPException(
            detail='user not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_404_NOT_FOUND)
        

@router.get('/all/{limit}', status_code=status.HTTP_200_OK)
async def get_all_users(
    user_service: Annotated[UsersService, Depends(users_service)],
    limit: int
):
    try:
        users = await user_service.get_all(limit)
        if users:
            return users
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='users not found'
        )
        
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

