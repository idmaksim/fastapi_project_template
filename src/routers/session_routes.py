from sqlalchemy.orm import Session
from db import get_db
import table_models
import request_models
from sqlalchemy import or_, and_
from typing import List
from random import randint

from datetime import time

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix='/sessions',
    tags=['Sessions']
)


@router.get('/share')
async def get_session_by_code(
    share_code: int,
    db: Session = Depends(get_db)
):
    session = db.query(table_models.Sessions).filter(
        table_models.Sessions.share_code == share_code
            
    ).first()
    
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='sessions not found'
        )
        
    session_exercises = list()
    
    exercises: List[table_models.SessionExercises] = db.query(table_models.SessionExercises).filter(
        table_models.SessionExercises.session_id == session.id
    ).all()
    
    for exercise in exercises:
        session_exercises.append(
            dict(
                exercise_id=exercise.exercise_id,
                sets=exercise.sets,
                reps=exercise.reps
            )
        )
        
    session.__dict__['exercises'] = session_exercises
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=jsonable_encoder(session)
        )
    )


@router.get('')
async def get_sessions(
    user_id: int,
    db: Session = Depends(get_db)
):
    sessions = db.query(table_models.Sessions).filter(
        or_(
            table_models.Sessions.user_id == user_id,
            table_models.Sessions.user_id == 0,
            
        )
    ).all()
    
    if sessions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='sessions not found'
        )
    
    sessions_data = list()
    
    for session in sessions:    
        session_exercises = list()
        
        exercises: List[table_models.SessionExercises] = db.query(table_models.SessionExercises).filter(
            table_models.SessionExercises.session_id == session.id
        ).all()
        
        for exercise in exercises:
            session_exercises.append(
                dict(
                    exercise_id=exercise.exercise_id,
                    sets=exercise.sets,
                    reps=exercise.reps
                )
            )
            
        session.__dict__['exercises'] = session_exercises
        sessions_data.append(
            session.__dict__
        )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            data=jsonable_encoder(sessions_data)
        )
    )


@router.post('')
async def add_session(
    session: request_models.SessionRequest,
    db: Session = Depends(get_db)
):
    session_json = session.model_dump()
    
    share_code = randint(10000000, 99999999)
    
    while (
        db.query(table_models.Sessions).filter(
            table_models.Sessions.share_code == share_code
        ).first()
    ):
        share_code = randint(10000000, 99999999)
    
    new_session = table_models.Sessions(
        user_id=session_json['user_id'],
        name=session_json['name'],
        created_at=session_json['created_at'],
        time_length=time(minute=int(session_json['time_length']/60)),
        share_code=share_code
    )
      
    try:
        db.add(new_session)

        db.commit()
        db.refresh(new_session)
        
        for exercise in session_json['exercises']:
            new_exercise = table_models.SessionExercises(
                session_id=new_session.id,
                exercise_id=exercise['exercise_id'],
                sets=exercise['sets'],
                reps=exercise['reps'],
            )
            
            db.add(new_exercise)
            db.commit()
            
        db.refresh(new_session)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=jsonable_encoder(new_session)
            )
        )    
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{error}'
        )


@router.put('')
async def update_session(
    session_id: int,
    session: request_models.SessionRequest,
    db: Session = Depends(get_db)
):
    
    query = db.query(table_models.Sessions).filter(
        table_models.Sessions.id == session_id
    )
    old_session = query.first()
    
    if old_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='session not found'
        )
    
    session_json = session.model_dump()
    
    new_session = dict(
        user_id=session_json['user_id'],
        name=session_json['name'],
        created_at=session_json['created_at'],
        time_length=time(minute=int(session_json['time_length']/60)),
        share_code=old_session.share_code
    )
        
    session_exercises = db.query(table_models.SessionExercises).filter(
        table_models.SessionExercises.session_id == session_id
    ).all()
    
    for exercise in session_exercises:
        db.delete(exercise)
        db.commit()
        
    query.update(new_session, synchronize_session=False)
    db.commit()

    
    try:    
        
        for exercise in session_json['exercises']:
            new_exercise = table_models.SessionExercises(
                session_id=session_id,
                exercise_id=exercise['exercise_id'],
                sets=exercise['sets'],
                reps=exercise['reps'],
            )
            
            db.add(new_exercise)
            db.commit()
        
        new_session['id'] = session_id
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                data=jsonable_encoder(new_session)
            )
        )    

    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{error}'
        )
