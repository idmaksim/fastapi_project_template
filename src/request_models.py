from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class UserRequest(BaseModel):
    email: str = Field(max_length=40, min_length=5)
    password: str = Field(max_length=30, min_length=6)
    name: str = Field(max_length=30, min_length=2)
    gender_id: int = Field(gt=0, default=1)


class MuscleGroupRequest(BaseModel):
    name: str = Field(min_length=3, max_length=20)


class ExerciseInfoRequest(BaseModel):
    user_id: int = Field(ge=0)
    name: str = Field(min_length=3, max_length=30)
    muscle_group_id: int = Field(gt=0)
    instructions: str = Field(min_length=10)
    photo_name: str
    

class ExerciseRequest(BaseModel):
    exercise_id: int = Field(gt=0)
    sets: int = Field(gt=0)
    reps: int = Field(gt=0)


class SessionRequest(BaseModel):
    user_id: int = Field(ge=0)
    name: str = Field(min_length=2, max_length=30)
    created_at: datetime
    time_length: int
    
    exercises: List[ExerciseRequest]