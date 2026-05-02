from sqlalchemy import Column, Enum, Integer, String, DateTime,ForeignKey,Float,Enum
from database import Base
from datetime import datetime


class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    daily_calorie_limit_id = Column(Integer, ForeignKey("daily_calorie_limits.id"))
    daily_calorie_limit = Float()
    today_calories = Float()
    difference_calories = Float()
    state = Column(
                Enum("draft", "submit", "cancel", name="state_enum"),
                default="draft",
                nullable=False
            )


class FoodLine(Base):
    __tablename__ = "food_lines"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id"))
    diet_id = Column(Integer, ForeignKey("diets.id"))
    quantity = Column(Integer)
    calories = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))


class ExerciseLine(Base):
    __tablename__ = "exercise_lines"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    duration_minutes = Column(Integer)
    calories_burned = Column(Float)
    diet_id = Column(Integer, ForeignKey("diets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class DailyCalorieLimit(Base):
    __tablename__ = "daily_calorie_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)
    calorie_limit = Column(Float)