from sqlalchemy import Column, Integer, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, index=True, nullable=False)
    full_name = Column(String(256), nullable=False)
    password_hash = Column(String(256), nullable=False)
