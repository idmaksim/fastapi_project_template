from sqlalchemy.orm import Session
from db import get_db
import table_models
import request_models
from sqlalchemy import or_

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix='/exercises',
    tags=['Exercises']
)


@router.get('')
async def get_exercises(
    user_id: int,
    db: Session = Depends(get_db)
):
    exercises = db.query(table_models.Exercises).filter(
        or_(
            user_id == table_models.Exercises.user_id,
            0 == table_models.Exercises.user_id
        )
    ).all()

    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User doesn\'t have any exercises'
        )

    exercises_data = []
    for exercise in exercises:
        exercise_data = jsonable_encoder(exercise)
        exercise_data['muscle_group'] = exercise.muscle_group
        del exercise_data['muscle_group_id']
        exercises_data.append(exercise_data)
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=jsonable_encoder(exercises_data)
        )
    )


@router.post('')
async def add_exercise(
    exercise: request_models.ExerciseInfoRequest,
    db: Session = Depends(get_db)
):
    new_exercise = table_models.Exercises(**exercise.model_dump())
    try:
        db.add(new_exercise)

        db.commit()
        db.refresh(new_exercise)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=jsonable_encoder(new_exercise)
            )
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{error}'
        )
