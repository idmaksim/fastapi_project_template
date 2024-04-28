from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import table_models 
import request_models
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import or_


router = APIRouter(
    prefix='/muscle_groups',
    tags=['Muscle Gropus']
)


@router.post('')
async def add_muscle_group(
    muscle_group: request_models.MuscleGroupRequest,
    db: Session = Depends(get_db)
):
    new_muscle_group = table_models.MuscleGroups(**muscle_group.model_dump())

    try:
        db.add(new_muscle_group)

        db.commit()
        db.refresh(new_muscle_group)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=jsonable_encoder(new_muscle_group)
            )
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{error}'
        )
    
    
@router.get('/all')
async def all_muscle_gorups_get(
    db: Session = Depends(get_db)
):
    muscle_groups = db.query(table_models.MuscleGroups).all()

    if not muscle_groups:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="muscle_groups not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=jsonable_encoder(muscle_groups)
        )
    )