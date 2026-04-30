from sqlalchemy import Column, Float, Integer, String

from app.db.base import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    category = Column(String(128), nullable=False)
    qty_gram = Column(Float, nullable=False)
    calories = Column(Float, nullable=False)
