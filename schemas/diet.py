from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseResponse(ExerciseBase):
    id: int

    class Config:
        from_attributes = True


class DailyCalorieLimitBase(BaseModel):
    calorie_limit: float


class DailyCalorieLimitCreate(DailyCalorieLimitBase):
    pass


class DailyCalorieLimitResponse(DailyCalorieLimitBase):
    id: int
    user_id: int
    start_date: datetime
    end_date: datetime
    state: str

    class Config:
        from_attributes = True


class FoodBase(BaseModel):
    name: str
    calories: float


class FoodCreate(FoodBase):
    pass


class FoodResponse(FoodBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class FoodLineBase(BaseModel):
    food_id: int
    quantity: int
    calories: float


class FoodLineCreate(FoodLineBase):
    pass


class FoodLineResponse(FoodLineBase):
    id: int
    diet_id: int
    user_id: int

    class Config:
        from_attributes = True


class ExerciseLineBase(BaseModel):
    exercise_id: int
    duration_minutes: int
    calories_burned: float


class ExerciseLineCreate(ExerciseLineBase):
    pass


class ExerciseLineResponse(ExerciseLineBase):
    id: int
    diet_id: int
    user_id: int

    class Config:
        from_attributes = True


class DietBase(BaseModel):
    name: str
    daily_calorie_limit: Optional[float] = None
    today_calories: Optional[float] = 0
    state: str = "draft"


class DietCreate(BaseModel):
    name: str
    daily_calorie_limit: Optional[float] = None
    state: str = "draft"


class DietUpdate(BaseModel):
    name: Optional[str] = None
    today_calories: Optional[float] = None
    difference_calories: Optional[float] = None
    state: Optional[str] = None


class DietResponse(DietBase):
    id: int
    user_id: int
    created_at: datetime
    difference_calories: Optional[float]
    food_lines: List[FoodLineResponse] = []
    exercise_lines: List[ExerciseLineResponse] = []

    class Config:
        from_attributes = True
