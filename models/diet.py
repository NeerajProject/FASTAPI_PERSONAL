from sqlalchemy import Column, Enum, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily_calorie_limit_id = Column(Integer, ForeignKey("daily_calorie_limits.id"), nullable=True)
    daily_calorie_limit = Column(Float, nullable=True)
    today_calories = Column(Float, default=0)
    difference_calories = Column(Float, nullable=True)
    state = Column(
        Enum("draft", "submit", "cancel", name="state_enum"),
        default="draft",
        nullable=False
    )
    
    # One-to-many relationships with cascade delete
    user = relationship("User", back_populates="diets")
    food_lines = relationship(
        "FoodLine",
        back_populates="diet",
        cascade="all, delete-orphan",
        lazy="select",
        foreign_keys="FoodLine.diet_id"
    )
    exercise_lines = relationship(
        "ExerciseLine",
        back_populates="diet",
        cascade="all, delete-orphan",
        lazy="select",
        foreign_keys="ExerciseLine.diet_id"
    )


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    calories = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class FoodLine(Base):
    __tablename__ = "food_lines"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    diet_id = Column(Integer, ForeignKey("diets.id"), nullable=False)
    quantity = Column(Integer, default=1)
    calories = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Many-to-one relationships
    diet = relationship(
        "Diet",
        back_populates="food_lines",
        foreign_keys=[diet_id]
    )
    food = relationship("Food", lazy="select")
    user = relationship("User", lazy="select")


class ExerciseLine(Base):
    __tablename__ = "exercise_lines"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    duration_minutes = Column(Integer)
    calories_burned = Column(Float)
    diet_id = Column(Integer, ForeignKey("diets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Many-to-one relationships
    diet = relationship(
        "Diet",
        back_populates="exercise_lines",
        foreign_keys=[diet_id]
    )
    exercise = relationship("Exercise", lazy="select")
    user = relationship("User", lazy="select")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DailyCalorieLimit(Base):
    __tablename__ = "daily_calorie_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)
    calorie_limit = Column(Float)
    state = Column(
        Enum("draft", "submit", "cancel", name="state_enum"),
        default="draft",
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", lazy="select")