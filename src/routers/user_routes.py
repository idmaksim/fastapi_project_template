from db import get_db
from sqlalchemy.orm import Session
import table_models 
import request_models 
from fastapi import Depends, APIRouter, HTTPException


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get('')
async def user_get(email: str, password: str,
                   db: Session = Depends(get_db)):

    user = db.query(table_models.Users).filter(
        table_models.Users.email == email
    ).filter(
        table_models.Users.password == password
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail='user not found'
        )

    return dict(
        data=user
    )


@router.post('')
async def user_add(user: request_models.UserRequest,
                   db: Session = Depends(get_db)):

    new_user = table_models.Users(**user.model_dump())

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

        return dict(
            data=new_user
        )

    except:
        raise HTTPException(
            status_code=409,
            detail='cant add user'
        )


@router.put('')
async def user_update(email: str, password: str,
                      new_user: request_models.UserRequest,
                      db: Session = Depends(get_db)):

    query = db.query(table_models.Users).filter(table_models.Users.email == email).filter(
        table_models.Users.password == password)

    old_user = query.first()

    if old_user is None:
        raise HTTPException(
            status_code=404,
            detail='user not found'
        )

    query.update(new_user.model_dump(), synchronize_session=False)

    try:
        db.commit()

        updated_user = db.query(table_models.Users).filter(
            table_models.Users.email == new_user.email
        ).filter(
            table_models.Users.password == new_user.password
        ).first()

        return dict(
            data=updated_user
        )
    except:
        raise HTTPException(
            status_code=304,
            detail='cant update user'
        )


@router.delete('')
async def user_delete(email: str, password: str,
                      db: Session = Depends(get_db)):

    user = db.query(table_models.Users).filter(
        table_models.Users.email == email
    ).filter(
        table_models.Users.password == password
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail='user not found'
        )

    db.delete(user)
    db.commit()

    return dict(
        data=user
    )

@router.get('/names')
async def all_usernames_get(db: Session = Depends(get_db)):
    users = db.query(table_models.Users).all()
    usernames = [user.name for user in users]

    if not usernames:
        raise HTTPException(
            status_code=404,
            detail="users not found"
        )

    return dict(
        data=usernames
    )
    