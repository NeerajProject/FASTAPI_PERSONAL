from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.diet import Diet, Food, FoodLine, ExerciseLine, Exercise, DailyCalorieLimit
from schemas.diet import DietCreate, DietUpdate, FoodCreate, FoodLineCreate, ExerciseLineCreate, ExerciseCreate, DailyCalorieLimitCreate

class DietRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, diet: DietCreate, user_id: int) -> Diet:
        db_diet = Diet(
            name=diet.name,
            user_id=user_id,
            daily_calorie_limit=diet.daily_calorie_limit,
            state=diet.state
        )
        self.db.add(db_diet)
        await self.db.commit()
        await self.db.refresh(db_diet)
        return db_diet

    async def get(self, diet_id: int) -> Diet | None:
        result = await self.db.execute(select(Diet).filter(Diet.id == diet_id))
        return result.scalar_one_or_none()

    async def get_all_for_user(self, user_id: int) -> list[Diet]:
        result = await self.db.execute(select(Diet).filter(Diet.user_id == user_id))
        return result.scalars().all()

    async def update(self, diet_id: int, diet: DietUpdate) -> Diet | None:
        db_diet = await self.get(diet_id)
        if db_diet:
            if diet.name is not None:
                db_diet.name = diet.name
            if diet.today_calories is not None:
                db_diet.today_calories = diet.today_calories
            if diet.difference_calories is not None:
                db_diet.difference_calories = diet.difference_calories
            if diet.state is not None:
                db_diet.state = diet.state
            await self.db.commit()
            await self.db.refresh(db_diet)
        return db_diet

    async def delete(self, diet_id: int) -> bool:
        db_diet = await self.get(diet_id)
        if db_diet:
            await self.db.delete(db_diet)
            await self.db.commit()
            return True
        return False

    async def update_calorie_calculation(self, diet_id: int) -> Diet | None:
        db_diet = await self.get(diet_id)
        if db_diet:
            food_result = await self.db.execute(select(func.sum(FoodLine.calories)).filter(FoodLine.diet_id == diet_id))
            total_food_calories = food_result.scalar() or 0
            
            exercise_result = await self.db.execute(select(func.sum(ExerciseLine.calories_burned)).filter(ExerciseLine.diet_id == diet_id))
            total_burned_calories = exercise_result.scalar() or 0
            
            db_diet.today_calories = total_food_calories
            if db_diet.daily_calorie_limit:
                db_diet.difference_calories = db_diet.daily_calorie_limit - total_food_calories + total_burned_calories
            
            await self.db.commit()
            await self.db.refresh(db_diet)
        return db_diet


class FoodRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, food: FoodCreate, user_id: int) -> Food:
        db_food = Food(name=food.name, calories=food.calories, user_id=user_id)
        self.db.add(db_food)
        await self.db.commit()
        await self.db.refresh(db_food)
        return db_food

    async def get(self, food_id: int) -> Food | None:
        result = await self.db.execute(select(Food).filter(Food.id == food_id))
        return result.scalar_one_or_none()

    async def get_all_for_user(self, user_id: int) -> list[Food]:
        result = await self.db.execute(select(Food).filter(Food.user_id == user_id))
        return result.scalars().all()

    async def delete(self, food_id: int) -> bool:
        db_food = await self.get(food_id)
        if db_food:
            await self.db.delete(db_food)
            await self.db.commit()
            return True
        return False


class FoodLineRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, food_line: FoodLineCreate, diet_id: int, user_id: int) -> FoodLine:
        db_food_line = FoodLine(
            food_id=food_line.food_id,
            diet_id=diet_id,
            quantity=food_line.quantity,
            calories=food_line.calories,
            user_id=user_id
        )
        self.db.add(db_food_line)
        await self.db.commit()
        await self.db.refresh(db_food_line)
        return db_food_line

    async def get(self, food_line_id: int) -> FoodLine | None:
        result = await self.db.execute(select(FoodLine).filter(FoodLine.id == food_line_id))
        return result.scalar_one_or_none()

    async def get_all_for_diet(self, diet_id: int) -> list[FoodLine]:
        result = await self.db.execute(select(FoodLine).filter(FoodLine.diet_id == diet_id))
        return result.scalars().all()

    async def update(self, food_line_id: int, quantity: int, calories: float) -> FoodLine | None:
        db_food_line = await self.get(food_line_id)
        if db_food_line:
            db_food_line.quantity = quantity
            db_food_line.calories = calories
            await self.db.commit()
            await self.db.refresh(db_food_line)
        return db_food_line

    async def delete(self, food_line_id: int) -> bool:
        db_food_line = await self.get(food_line_id)
        if db_food_line:
            await self.db.delete(db_food_line)
            await self.db.commit()
            return True
        return False


class ExerciseLineRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, exercise_line: ExerciseLineCreate, diet_id: int, user_id: int) -> ExerciseLine:
        db_exercise_line = ExerciseLine(
            exercise_id=exercise_line.exercise_id,
            duration_minutes=exercise_line.duration_minutes,
            calories_burned=exercise_line.calories_burned,
            diet_id=diet_id,
            user_id=user_id
        )
        self.db.add(db_exercise_line)
        await self.db.commit()
        await self.db.refresh(db_exercise_line)
        return db_exercise_line

    async def get(self, exercise_line_id: int) -> ExerciseLine | None:
        result = await self.db.execute(select(ExerciseLine).filter(ExerciseLine.id == exercise_line_id))
        return result.scalar_one_or_none()

    async def get_all_for_diet(self, diet_id: int) -> list[ExerciseLine]:
        result = await self.db.execute(select(ExerciseLine).filter(ExerciseLine.id == diet_id))
        return result.scalars().all()

    async def delete(self, exercise_line_id: int) -> bool:
        db_exercise_line = await self.get(exercise_line_id)
        if db_exercise_line:
            await self.db.delete(db_exercise_line)
            await self.db.commit()
            return True
        return False


class ExerciseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, exercise: ExerciseCreate) -> Exercise:
        db_exercise = Exercise(name=exercise.name)
        self.db.add(db_exercise)
        await self.db.commit()
        await self.db.refresh(db_exercise)
        return db_exercise

    async def get(self, exercise_id: int) -> Exercise | None:
        result = await self.db.execute(select(Exercise).filter(Exercise.id == exercise_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Exercise]:
        result = await self.db.execute(select(Exercise))
        return result.scalars().all()

    async def delete(self, exercise_id: int) -> bool:
        db_exercise = await self.get(exercise_id)
        if db_exercise:
            await self.db.delete(db_exercise)
            await self.db.commit()
            return True
        return False


class DailyCalorieLimitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, daily_limit: DailyCalorieLimitCreate, user_id: int) -> DailyCalorieLimit:
        db_limit = DailyCalorieLimit(
            user_id=user_id,
            calorie_limit=daily_limit.calorie_limit
        )
        self.db.add(db_limit)
        await self.db.commit()
        await self.db.refresh(db_limit)
        return db_limit

    async def get_for_user(self, user_id: int) -> DailyCalorieLimit | None:
        result = await self.db.execute(select(DailyCalorieLimit).filter(DailyCalorieLimit.user_id == user_id))
        return result.scalar_one_or_none()

    async def delete(self, limit_id: int) -> bool:
        result = await self.db.execute(select(DailyCalorieLimit).filter(DailyCalorieLimit.id == limit_id))
        db_limit = result.scalar_one_or_none()
        if db_limit:
            await self.db.delete(db_limit)
            await self.db.commit()
            return True
        return False
