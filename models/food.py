from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    caloried    = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

