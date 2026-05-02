from pydantic import BaseModel
from datetime import datetime


class DietBase(BaseModel):
    name: str


class DietCreate(DietBase):
    pass


class DietUpdate(BaseModel):
    name: str | None = None


class DietResponse(DietBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
