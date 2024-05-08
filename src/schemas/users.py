from pydantic import BaseModel, Field


class UserAddRequest(BaseModel):
    email: str = Field(max_length=40, min_length=5)
    password: str = Field(max_length=30, min_length=6)
    name: str = Field(max_length=30, min_length=2)
    username: str
    
