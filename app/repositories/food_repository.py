from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.food_item import FoodItem
from app.schemas.food import FoodCreate


class FoodRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[FoodItem]:
        return self.db.query(FoodItem).all()

    def get(self, food_id: int) -> Optional[FoodItem]:
        return self.db.query(FoodItem).filter(FoodItem.id == food_id).first()

    def create(self, food_in: FoodCreate) -> FoodItem:
        food = FoodItem(**food_in.dict())
        self.db.add(food)
        self.db.commit()
        self.db.refresh(food)
        return food
