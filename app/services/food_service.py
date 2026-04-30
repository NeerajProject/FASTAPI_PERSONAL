from typing import List, Optional

from app.models.food_item import FoodItem
from app.repositories.food_repository import FoodRepository
from app.schemas.food import FoodCreate


class FoodService:
    def __init__(self, repository: FoodRepository):
        self.repository = repository

    def get_foods(self) -> List[FoodItem]:
        return self.repository.get_all()

    def get_food(self, food_id: int) -> Optional[FoodItem]:
        return self.repository.get(food_id)

    def create_food(self, food_in: FoodCreate) -> FoodItem:
        return self.repository.create(food_in)
