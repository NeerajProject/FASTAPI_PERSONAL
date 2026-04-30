from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.food_repository import FoodRepository
from app.schemas.food import FoodCreate, FoodRead
from app.services.food_service import FoodService

router = APIRouter()


@router.get("/food-master", response_model=List[FoodRead])
def list_food(db: Session = Depends(get_db)) -> List[FoodRead]:
    """Return all food master items."""
    service = FoodService(FoodRepository(db))
    return service.get_foods()


@router.post("/food-master", response_model=FoodRead, status_code=status.HTTP_201_CREATED)
def create_food_item(food_in: FoodCreate, db: Session = Depends(get_db)) -> FoodRead:
    """Create a new food master record.

    Request body:
    {
      "name": "Apple",
      "category": "Fruit",
      "qty_gram": 150.0,
      "calories": 95.0
    }
    """
    service = FoodService(FoodRepository(db))
    return service.create_food(food_in)
