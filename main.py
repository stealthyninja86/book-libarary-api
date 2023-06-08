from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(bind = engine)

def get_db():
    try: 
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=10)


BOOKS = []


@app.get("/")
async def list_books(db: Session = Depends(get_db)):
    return db.query(model.Books).all()


@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = model.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()
    return book


@app.put("/update_book/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(model.Books).filter(model.Books.id == book_id).first()
    
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id}: does not exist"
        )
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()
    return book


@app.delete("/delete_book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(model.Books).filter(model.Books.id == book_id).first()


    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID : {book_id} does not exist"
        )
    db.query(model.Books).filter(model.Books.id == book_id).delete()
    db.commit()
