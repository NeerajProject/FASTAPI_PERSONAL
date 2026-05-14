from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from models.user import User
from routers.users import get_current_user
from repositories.diet_repository import (
    DietRepository, FoodRepository, FoodLineRepository,
    ExerciseLineRepository, ExerciseRepository, DailyCalorieLimitRepository
)
from schemas.diet import (
    DietCreate, DietUpdate, DietResponse, FoodCreate, FoodResponse,
    FoodLineCreate, FoodLineResponse, ExerciseLineCreate, ExerciseLineResponse,
    ExerciseCreate, ExerciseResponse, DailyCalorieLimitCreate, DailyCalorieLimitResponse
)

router = APIRouter(prefix="/diets", tags=["diets"])


# ============ DIET ENDPOINTS ============

@router.post("/", response_model=DietResponse)
async def create_diet(
    diet: DietCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new diet - requires authentication"""
    repo = DietRepository(db)
    return await repo.create(diet, current_user.id)


@router.get("/", response_model=list[DietResponse])
async def get_all_diets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all diets for the current user - requires authentication"""
    repo = DietRepository(db)
    return await repo.get_all_for_user(current_user.id)


@router.get("/{diet_id}", response_model=DietResponse)
async def get_diet(
    diet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific diet by ID - requires authentication"""
    repo = DietRepository(db)
    diet = await repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this diet")
    return diet


@router.put("/{diet_id}", response_model=DietResponse)
async def update_diet(
    diet_id: int,
    diet: DietUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update a diet - requires authentication"""
    repo = DietRepository(db)
    db_diet = await repo.get(diet_id)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if db_diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this diet")
    return await repo.update(diet_id, diet)


@router.delete("/{diet_id}")
async def delete_diet(
    diet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a diet - requires authentication"""
    repo = DietRepository(db)
    db_diet = await repo.get(diet_id)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if db_diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this diet")
    await repo.delete(diet_id)
    return {"message": "Diet deleted successfully"}


# ============ FOOD ENDPOINTS ============

@router.post("/foods/", response_model=FoodResponse)
async def create_food(
    food: FoodCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new food entry - requires authentication"""
    repo = FoodRepository(db)
    return await repo.create(food, current_user.id)


@router.get("/foods/", response_model=list[FoodResponse])
async def get_all_foods(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all foods for the current user - requires authentication"""
    repo = FoodRepository(db)
    return await repo.get_all_for_user(current_user.id)


@router.delete("/foods/{food_id}")
async def delete_food(
    food_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a food entry - requires authentication"""
    repo = FoodRepository(db)
    food = await repo.get(food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    if food.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this food")
    await repo.delete(food_id)
    return {"message": "Food deleted successfully"}


# ============ FOOD LINE ENDPOINTS ============

@router.post("/{diet_id}/food-lines/", response_model=FoodLineResponse)
async def add_food_line(
    diet_id: int,
    food_line: FoodLineCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Add food line to a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this diet")
    
    repo = FoodLineRepository(db)
    food_line_created = await repo.create(food_line, diet_id, current_user.id)
    await diet_repo.update_calorie_calculation(diet_id)
    return food_line_created


@router.get("/{diet_id}/food-lines/", response_model=list[FoodLineResponse])
async def get_food_lines(
    diet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get food lines for a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this diet")
    
    repo = FoodLineRepository(db)
    return await repo.get_all_for_diet(diet_id)


@router.put("/{diet_id}/food-lines/{food_line_id}", response_model=FoodLineResponse)
async def update_food_line(
    diet_id: int,
    food_line_id: int,
    food_line: FoodLineCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Update a food line in a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this diet")
    
    repo = FoodLineRepository(db)
    existing_food_line = await repo.get(food_line_id)
    if not existing_food_line:
        raise HTTPException(status_code=404, detail="Food line not found")
    
    updated = await repo.update(food_line_id, food_line.quantity, food_line.calories)
    await diet_repo.update_calorie_calculation(diet_id)
    return updated


@router.delete("/{diet_id}/food-lines/{food_line_id}")
async def delete_food_line(
    diet_id: int,
    food_line_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a food line from a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this diet")
    
    repo = FoodLineRepository(db)
    food_line = await repo.get(food_line_id)
    if not food_line:
        raise HTTPException(status_code=404, detail="Food line not found")
    await repo.delete(food_line_id)
    await diet_repo.update_calorie_calculation(diet_id)
    return {"message": "Food line deleted successfully"}


# ============ EXERCISE LINE ENDPOINTS ============

@router.post("/{diet_id}/exercise-lines/", response_model=ExerciseLineResponse)
async def add_exercise_line(
    diet_id: int,
    exercise_line: ExerciseLineCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Add exercise line to a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this diet")
    
    repo = ExerciseLineRepository(db)
    exercise_line_created = await repo.create(exercise_line, diet_id, current_user.id)
    await diet_repo.update_calorie_calculation(diet_id)
    return exercise_line_created


@router.get("/{diet_id}/exercise-lines/", response_model=list[ExerciseLineResponse])
async def get_exercise_lines(
    diet_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get exercise lines for a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this diet")
    
    repo = ExerciseLineRepository(db)
    return await repo.get_all_for_diet(diet_id)


@router.delete("/{diet_id}/exercise-lines/{exercise_line_id}")
async def delete_exercise_line(
    diet_id: int,
    exercise_line_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete an exercise line from a diet - requires authentication"""
    diet_repo = DietRepository(db)
    diet = await diet_repo.get(diet_id)
    if not diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    if diet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this diet")
    
    repo = ExerciseLineRepository(db)
    exercise_line = await repo.get(exercise_line_id)
    if not exercise_line:
        raise HTTPException(status_code=404, detail="Exercise line not found")
    await repo.delete(exercise_line_id)
    await diet_repo.update_calorie_calculation(diet_id)
    return {"message": "Exercise line deleted successfully"}


# ============ EXERCISE ENDPOINTS ============

@router.post("/exercises/", response_model=ExerciseResponse)
async def create_exercise(
    exercise: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new exercise - requires authentication"""
    repo = ExerciseRepository(db)
    return await repo.create(exercise)


@router.get("/exercises/", response_model=list[ExerciseResponse])
async def get_all_exercises(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all exercises - requires authentication"""
    repo = ExerciseRepository(db)
    return await repo.get_all()


@router.delete("/exercises/{exercise_id}")
async def delete_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete an exercise - requires authentication"""
    repo = ExerciseRepository(db)
    exercise = await repo.get(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    await repo.delete(exercise_id)
    return {"message": "Exercise deleted successfully"}


# ============ DAILY CALORIE LIMIT ENDPOINTS ============

@router.post("/daily-limits/", response_model=DailyCalorieLimitResponse)
async def set_daily_calorie_limit(
    daily_limit: DailyCalorieLimitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Set daily calorie limit - requires authentication"""
    repo = DailyCalorieLimitRepository(db)
    return await repo.create(daily_limit, current_user.id)


@router.get("/daily-limits/", response_model=DailyCalorieLimitResponse)
async def get_daily_calorie_limit(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current daily calorie limit - requires authentication"""
    repo = DailyCalorieLimitRepository(db)
    limit = await repo.get_for_user(current_user.id)
    if not limit:
        raise HTTPException(status_code=404, detail="Daily calorie limit not set")
    return limit


@router.delete("/daily-limits/{limit_id}")
async def delete_daily_calorie_limit(
    limit_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete daily calorie limit - requires authentication"""
    repo = DailyCalorieLimitRepository(db)
    limit = await repo.get_for_user(current_user.id) # Wait, it was get(limit_id)
    # Re-checking repo... DailyCalorieLimitRepository has delete(limit_id)
    # I'll use get_for_user and check ID
    if not limit or limit.id != limit_id:
        raise HTTPException(status_code=404, detail="Daily calorie limit not found")
    if limit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this limit")
    await repo.delete(limit_id)
    return {"message": "Daily calorie limit deleted successfully"}
