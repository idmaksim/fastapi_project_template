from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from utils.dependencies import users_service
from schemas.user import UserCreate
from services.user import UserService
from utils.background_tasks import sample_bg_task


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserCreate,
    user_service: Annotated[UserService, Depends(users_service)],
    backdorund_tasks: BackgroundTasks
):

    backdorund_tasks.add_task(sample_bg_task, message=f'adding user {user}!')

    new_user = await user_service.add_user(user)
    if new_user:
        return new_user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user dont added')


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_service: Annotated[UserService, Depends(users_service)],
    id: int
):
    
    user = await user_service.get_one_by_id(id)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='user not found'
    )
        
            
        
@router.get('', status_code=status.HTTP_200_OK)
async def get_user(
    user_service: Annotated[UserService, Depends(users_service)],
    email: str,
    password: str
):
    user = await user_service.get_one(email=email, password=password)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='user not found'
    )
        
        

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_user_by_id(
    user_service: Annotated[UserService, Depends(users_service)],
    id: int
):

    user = await user_service.get_one_by_id(id)
    
    if user:
        deleted_user = await user_service.delete_by_id(id)
        return deleted_user
    
    raise HTTPException(
        detail='user not found',
        status_code=status.HTTP_404_NOT_FOUND
    )


  
@router.get('/all/{limit}', status_code=status.HTTP_200_OK)
async def get_all_users(
    user_service: Annotated[UserService, Depends(users_service)],
    limit: int
):
    users = await user_service.get_all(limit)
    if users:
        return users
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='users not found'
    )

