from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    email: str = Field(max_length=20, min_length=5)
    password: str = Field(max_length=20, min_length=6)
    name: str = Field(max_length=20, min_length=5)


class User(UserRequest):
    id: int = Field(gt=0)

    