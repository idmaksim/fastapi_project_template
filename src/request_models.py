from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class UserRequest(BaseModel):
    email: str = Field(max_length=40, min_length=5)
    password: str = Field(max_length=30, min_length=6)
    name: str = Field(max_length=30, min_length=2)
    gender_id: int = Field(gt=0, default=1)

