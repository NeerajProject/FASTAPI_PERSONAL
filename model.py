from database import Base
from sqlalchemy import Column, Integer, String, Date,VARCHAR

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_date = Column(Date)
    isbn = Column(String, unique=True, index=True)