from datetime import datetime
from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username: str
    registered_at: datetime = Field(default=datetime.now)
    role_id: int = Field(default=1)
    email: str
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool =Field(default=False)
