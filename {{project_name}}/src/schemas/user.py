from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(BaseUser):
    username: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseUser):
    pass


class UserResponse(BaseUser):
    id: int
    username: str
