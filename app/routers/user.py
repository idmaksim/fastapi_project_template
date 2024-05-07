from ..database import get_async_session
from ..table_models import User
from ..schemas import UserRequest

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import CursorResult, select


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    result: CursorResult = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "detail": 'ok', 
        "user": user
    }


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_user(new_user: UserRequest, session: AsyncSession = Depends(get_async_session)):
    user = User(**new_user.model_dump()) 
    try:

        session.add(user)
        await session.commit()  
        await session.refresh(user)  
        
        del user.__dict__['hashed_password']

        return {
            'data': user,
            'detail': 'ok'
        }
    except Exception as e:
        raise HTTPException(
            detail=jsonable_encoder(e),
            status_code=status.HTTP_409_CONFLICT
        )
