from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    full_name: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
