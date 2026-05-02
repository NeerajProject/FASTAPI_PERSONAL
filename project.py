from fastapi import FastAPI,Depends
from database import get_db,engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel
from datetime import date   # ✅ import this

app = FastAPI()


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date
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


@app.get("/books/")
async def read_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books        

@app.get("/books/{book_id}")
async def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        return {"message": "Book not found"}
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        return {"message": "Book not found"}
    db.delete(book)
    db.commit()
    return {"message": f"Book with ID {book_id} deleted successfully."}


@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(model.Book).filter(model.Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")  # ✅ proper error

    db_book.title = book.title
    db_book.author = book.author
    db_book.published_date = book.published_date
    db_book.isbn = book.isbn

    db.commit()
    db.refresh(db_book)

    return db_book   # ✅ return updated object