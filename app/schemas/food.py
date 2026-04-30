from pydantic import BaseModel, Field


class FoodBase(BaseModel):
    name: str = Field(..., example="Apple")
    category: str = Field(..., example="Fruit")
    qty_gram: float = Field(..., example=150.0)
    calories: float = Field(..., example=95.0)


class FoodCreate(FoodBase):
    pass


class FoodRead(FoodBase):
    id: int

    class Config:
        orm_mode = True
