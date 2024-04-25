from db import get_db
import table_models 
import request_models 

from sqlalchemy import and_
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
from fastapi import Depends, APIRouter, HTTPException, status


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get('')
async def user_get(
        email: str, 
        password: str,
        db: Session = Depends(get_db)
    ):

    user = db.query(table_models.Users).filter(
        and_(
            table_models.Users.email == email,
            table_models.Users.password == password
        )
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=user
        )
    )


@router.post('')
async def user_add(
        user: request_models.UserRequest,
        db: Session = Depends(get_db)
    ):

    new_user = table_models.Users(**user.model_dump())

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=new_user
            )
        )
        
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error
        )


@router.put('')
async def user_update(
        email: str, 
        password: str,
        new_user: request_models.UserRequest,
        db: Session = Depends(get_db)
    ):

    query = db.query(table_models.Users).filter(
        and_(
            table_models.Users.email == email,
            table_models.Users.password == password
        )
    )
    old_user = query.first()
    if old_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    query.update(new_user.model_dump(), synchronize_session=False)

    try:
        db.commit()
        updated_user = db.query(table_models.Users).filter(
            and_(
                table_models.Users.email == new_user.email,
                table_models.Users.password == new_user.password
            )
        ).first()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=updated_user
            )
        )
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail=error
        )


@router.delete('')
async def user_delete(
        email: str, 
        password: str,
        db: Session = Depends(get_db)
    ):

    user = db.query(table_models.Users).filter(
        and_(
            table_models.Users.email == email,
            table_models.Users.password == password
        )
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )

    db.delete(user)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=user
        )
    )


@router.get('/names')
async def all_usernames_get(
        db: Session = Depends(get_db)
    ):
    
    users = db.query(table_models.Users).all()
    usernames = [user.name for user in users]

    if not usernames:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="users not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=usernames
        )
    )
    