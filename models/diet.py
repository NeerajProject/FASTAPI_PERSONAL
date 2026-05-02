from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Float
from database import Base
from datetime import datetime


class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)




class FoodLine(Base):
    __tablename__ = "food_lines"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id"))
    diet_id = Column(Integer, ForeignKey("diets.id"))
    quantity = Column(Integer)
    calories = Column(Float)
