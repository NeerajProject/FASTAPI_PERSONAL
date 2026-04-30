from fastapi import APIRouter

from app.api.v1.food_master import router as food_master_router
from app.api.v1.users import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(food_master_router)
