from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.food_repository import FoodRepository
from app.schemas.food import FoodCreate, FoodRead
from app.services.food_service import FoodService

router = APIRouter()


@router.get("/food-master", response_model=List[FoodRead])
def list_food(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[FoodRead]:
    """Return all food master items.

    Route path: GET /api/v1/food-master
    Protected: requires Authorization header with Bearer token
    Example command:
      curl -X GET http://127.0.0.1:8000/api/v1/food-master \
        -H 'Authorization: Bearer <token>'
    """
    service = FoodService(FoodRepository(db))
    return service.get_foods()


@router.post("/food-master", response_model=FoodRead, status_code=status.HTTP_201_CREATED)
def create_food_item(
    food_in: FoodCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FoodRead:
    """Create a new food master record.

    Route path: POST /api/v1/food-master
    Protected: requires Authorization header with Bearer token
    Request body:
    {
      "name": "Apple",
      "category": "Fruit",
      "qty_gram": 150.0,
      "calories": 95.0
    }
    Example command:
      curl -X POST http://127.0.0.1:8000/api/v1/food-master \
        -H 'Authorization: Bearer <token>' \
        -H 'Content-Type: application/json' \
        -d '{"name":"Apple","category":"Fruit","qty_gram":150.0,"calories":95.0}'
    """
    service = FoodService(FoodRepository(db))
    return service.create_food(food_in)
