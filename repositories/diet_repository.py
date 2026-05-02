from sqlalchemy.orm import Session
from sqlalchemy import func
from models.diet import Diet, Food, FoodLine, ExerciseLine, Exercise, DailyCalorieLimit
from schemas.diet import DietCreate, DietUpdate, FoodCreate, FoodLineCreate, ExerciseLineCreate, ExerciseCreate, DailyCalorieLimitCreate


class DietRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, diet: DietCreate, user_id: int) -> Diet:
        """Create a new diet with user_id"""
        db_diet = Diet(
            name=diet.name,
            user_id=user_id,
            daily_calorie_limit=diet.daily_calorie_limit,
            state=diet.state
        )
        self.db.add(db_diet)
        self.db.flush()  # Get the ID without committing
        self.db.commit()
        self.db.refresh(db_diet)
        return db_diet

    def get(self, diet_id: int) -> Diet | None:
        """Get diet by ID with all relationships loaded"""
        return self.db.query(Diet).filter(Diet.id == diet_id).first()

    def get_all_for_user(self, user_id: int) -> list[Diet]:
        """Get all diets for a user with relationships"""
        return self.db.query(Diet).filter(Diet.user_id == user_id).all()

    def update(self, diet_id: int, diet: DietUpdate) -> Diet | None:
        """Update diet fields"""
        db_diet = self.get(diet_id)
        if db_diet:
            if diet.name is not None:
                db_diet.name = diet.name
            if diet.today_calories is not None:
                db_diet.today_calories = diet.today_calories
            if diet.difference_calories is not None:
                db_diet.difference_calories = diet.difference_calories
            if diet.state is not None:
                db_diet.state = diet.state
            self.db.commit()
            self.db.refresh(db_diet)
        return db_diet

    def delete(self, diet_id: int) -> bool:
        """Delete diet and all associated food_lines and exercise_lines (cascade)"""
        db_diet = self.get(diet_id)
        if db_diet:
            self.db.delete(db_diet)
            self.db.commit()
            return True
        return False

    def update_calorie_calculation(self, diet_id: int) -> Diet | None:
        """Recalculate total calories and difference for a diet"""
        db_diet = self.get(diet_id)
        if db_diet:
            total_food_calories = self.db.query(func.sum(FoodLine.calories)).filter(
                FoodLine.diet_id == diet_id
            ).scalar() or 0
            
            total_burned_calories = self.db.query(func.sum(ExerciseLine.calories_burned)).filter(
                ExerciseLine.diet_id == diet_id
            ).scalar() or 0
            
            db_diet.today_calories = total_food_calories
            if db_diet.daily_calorie_limit:
                db_diet.difference_calories = db_diet.daily_calorie_limit - total_food_calories + total_burned_calories
            
            self.db.commit()
            self.db.refresh(db_diet)
        return db_diet

    def add_food_line(self, diet_id: int, food_line: FoodLineCreate, user_id: int) -> FoodLine | None:
        """Add a food line to a diet and update calories"""
        db_diet = self.get(diet_id)
        if not db_diet:
            return None
        
        repo = FoodLineRepository(self.db)
        food_line_obj = repo.create(food_line, diet_id, user_id)
        self.update_calorie_calculation(diet_id)
        return food_line_obj

    def remove_food_line(self, diet_id: int, food_line_id: int) -> bool:
        """Remove a food line from a diet and update calories"""
        repo = FoodLineRepository(self.db)
        if repo.delete(food_line_id):
            self.update_calorie_calculation(diet_id)
            return True
        return False

    def add_exercise_line(self, diet_id: int, exercise_line: ExerciseLineCreate, user_id: int) -> ExerciseLine | None:
        """Add an exercise line to a diet and update calories"""
        db_diet = self.get(diet_id)
        if not db_diet:
            return None
        
        repo = ExerciseLineRepository(self.db)
        exercise_line_obj = repo.create(exercise_line, diet_id, user_id)
        self.update_calorie_calculation(diet_id)
        return exercise_line_obj

    def remove_exercise_line(self, diet_id: int, exercise_line_id: int) -> bool:
        """Remove an exercise line from a diet and update calories"""
        repo = ExerciseLineRepository(self.db)
        if repo.delete(exercise_line_id):
            self.update_calorie_calculation(diet_id)
            return True
        return False


class FoodRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, food: FoodCreate, user_id: int) -> Food:

        print(">>>>>>>>>",user_id)
        db_food = Food(name=food.name, calories=food.calories, user_id=user_id)
        self.db.add(db_food)
        self.db.commit()
        self.db.refresh(db_food)
        return db_food

    def get(self, food_id: int) -> Food | None:
        return self.db.query(Food).filter(Food.id == food_id).first()

    def get_all_for_user(self, user_id: int) -> list[Food]:
        return self.db.query(Food).filter(Food.user_id == user_id).all()

    def delete(self, food_id: int) -> bool:
        db_food = self.get(food_id)
        if db_food:
            self.db.delete(db_food)
            self.db.commit()
            return True
        return False


class FoodLineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, food_line: FoodLineCreate, diet_id: int, user_id: int) -> FoodLine:
        """Create a new food line entry"""
        db_food_line = FoodLine(
            food_id=food_line.food_id,
            diet_id=diet_id,
            quantity=food_line.quantity,
            calories=food_line.calories,
            user_id=user_id
        )
        self.db.add(db_food_line)
        self.db.commit()
        self.db.refresh(db_food_line)
        return db_food_line

    def get(self, food_line_id: int) -> FoodLine | None:
        """Get food line by ID"""
        return self.db.query(FoodLine).filter(FoodLine.id == food_line_id).first()

    def get_all_for_diet(self, diet_id: int) -> list[FoodLine]:
        """Get all food lines for a diet"""
        return self.db.query(FoodLine).filter(FoodLine.diet_id == diet_id).all()

    def update(self, food_line_id: int, quantity: int, calories: float) -> FoodLine | None:
        """Update food line quantity and calories"""
        db_food_line = self.get(food_line_id)
        if db_food_line:
            db_food_line.quantity = quantity
            db_food_line.calories = calories
            self.db.commit()
            self.db.refresh(db_food_line)
        return db_food_line

    def delete(self, food_line_id: int) -> bool:
        """Delete a food line (cascades if configured)"""
        db_food_line = self.get(food_line_id)
        if db_food_line:
            self.db.delete(db_food_line)
            self.db.commit()
            return True
        return False


class ExerciseLineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, exercise_line: ExerciseLineCreate, diet_id: int, user_id: int) -> ExerciseLine:
        """Create a new exercise line entry"""
        db_exercise_line = ExerciseLine(
            exercise_id=exercise_line.exercise_id,
            duration_minutes=exercise_line.duration_minutes,
            calories_burned=exercise_line.calories_burned,
            diet_id=diet_id,
            user_id=user_id
        )
        self.db.add(db_exercise_line)
        self.db.commit()
        self.db.refresh(db_exercise_line)
        return db_exercise_line

    def get(self, exercise_line_id: int) -> ExerciseLine | None:
        """Get exercise line by ID"""
        return self.db.query(ExerciseLine).filter(ExerciseLine.id == exercise_line_id).first()

    def get_all_for_diet(self, diet_id: int) -> list[ExerciseLine]:
        """Get all exercise lines for a diet"""
        return self.db.query(ExerciseLine).filter(ExerciseLine.diet_id == diet_id).all()

    def update(self, exercise_line_id: int, duration_minutes: int, calories_burned: float) -> ExerciseLine | None:
        """Update exercise line duration and calories burned"""
        db_exercise_line = self.get(exercise_line_id)
        if db_exercise_line:
            db_exercise_line.duration_minutes = duration_minutes
            db_exercise_line.calories_burned = calories_burned
            self.db.commit()
            self.db.refresh(db_exercise_line)
        return db_exercise_line

    def delete(self, exercise_line_id: int) -> bool:
        """Delete an exercise line (cascades if configured)"""
        db_exercise_line = self.get(exercise_line_id)
        if db_exercise_line:
            self.db.delete(db_exercise_line)
            self.db.commit()
            return True
        return False


class ExerciseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, exercise: ExerciseCreate) -> Exercise:
        db_exercise = Exercise(name=exercise.name)
        self.db.add(db_exercise)
        self.db.commit()
        self.db.refresh(db_exercise)
        return db_exercise

    def get(self, exercise_id: int) -> Exercise | None:
        return self.db.query(Exercise).filter(Exercise.id == exercise_id).first()

    def get_all(self) -> list[Exercise]:
        return self.db.query(Exercise).all()

    def delete(self, exercise_id: int) -> bool:
        db_exercise = self.get(exercise_id)
        if db_exercise:
            self.db.delete(db_exercise)
            self.db.commit()
            return True
        return False


class DailyCalorieLimitRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, daily_limit: DailyCalorieLimitCreate, user_id: int) -> DailyCalorieLimit:
        db_limit = DailyCalorieLimit(
            user_id=user_id,
            calorie_limit=daily_limit.calorie_limit
        )
        self.db.add(db_limit)
        self.db.commit()
        self.db.refresh(db_limit)
        return db_limit

    def get(self, limit_id: int) -> DailyCalorieLimit | None:
        return self.db.query(DailyCalorieLimit).filter(DailyCalorieLimit.id == limit_id).first()

    def get_for_user(self, user_id: int) -> DailyCalorieLimit | None:
        return self.db.query(DailyCalorieLimit).filter(DailyCalorieLimit.user_id == user_id).first()

    def delete(self, limit_id: int) -> bool:
        db_limit = self.get(limit_id)
        if db_limit:
            self.db.delete(db_limit)
            self.db.commit()
            return True
        return False
