from fastapi import FastAPI
from database import get_db,engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

app = FastAPI()


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: Date
    isbn: str

@app.post("/books/")
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = model.Book(
        title=book.title,
        author=book.author,
        published_date=book.published_date,
        isbn=book.isbn
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"message": f"Book '{db_book.title}' created successfully with ID {db_book.id}."}