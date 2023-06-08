- import fastapi and pydantic

```
from fastapi import FastAPI
from pydandtic import Basemodel, Field
from uuid import UUID
```

- create a basic app route

```
@app.get("/{name}")

async def read_api(name: str):

    return {"message": name}
```

- run the app using the command

```
uvicorn main:app --reload
```

- this will generate a link to access your api - http://127.0.0.1:8000/
- we can access the swagger docs to view all the request from the app - http://127.0.0.1:8000/docs

- using pydantic we can send a large amount of data in the form of a class to our api and specify the structure of data as well, by this we can define our data and assign datatypes max and min length, give aliases, decriptions etc

```
class Book(BaseModel):

    id: UUID

    title: str = Field(min_length = 1)

    author: str = Field(min_length =1, max_length=100)

    description: str= Field(min_length=1, max_length=100)

    rating: int = Field(gt = -1, lt =10)
```

- create books variable to store the list of books

```
BOOKS = []
```

- create a post route to for the create_books() which is used to add new books to the BOOKS variable

```
@app.post("/")

def create_book(book: Book):

    BOOKS.append(book)

    return book
```

- now we can go to the swagger docs using the link http://127.0.0.1:8000/docs and test our api

- create another function update_books() to update or change the book using its UUID, if the book does not exist then raise and exception

```
@app.post("/search_book/{book_id}")

def update_book(book_id: UUID, book: Book):

    counter = 0

    for x in BOOKS:

        counter += 1

        if x.id == book_id:

            BOOKS[counter - 1] = book

            return BOOKS[counter - 1]

    raise HTTPException(

        status_code=404,

        detail=f"ID {book_id}: does not exist"

    )
```

- create another function to delete the books in BOOKS

```
@app.post("/delete_book/{book_id}")

def delete_book(book_id: UUID):

    counter = 0

    for x in BOOKS:

        counter += 1

        if x.id == book_id:

            del BOOKS[counter-1]

            return f"ID: {book_id} deleted"

    raise HTTPException(

        status_code=404,

        detail=f"ID : {book_id} does not exist"

    )
```

- the problem with using a list is that it resets everytime we reload a session, to solve this problem we will create a database to store our records
- create a new file database.py, include the following imports

```
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
```

- create a database using sqlalchemy

```
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
```

- create engine, sessionlocal and base

```
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()
```

- create a new file model.py, here we define the database model

```
from sqlalchemy import Column, Integer, String

from database import Base



class Books(Base):

    __tablename__ = 'books'



    id = Column(Integer, primary_key = True, index = True)

    title = Column(String)

    author = Column(String)

    description = Column(String)

    rating = Column(Integer)
```

- after this we import model.py and database.py into main.py

```
import model

from database import engine, SessionLocal3

from sqlalchemy.orm import Session


model.Base.metadata.create_all(bind = engine)
```

`model.Base.metadata.create_all(bind=engine)` line is used to create the tables defined in your models.

- closing a database connection

```
def get_db():

    try:

        db = SessionLocal()

        yield db

    finally:

        db.close()
```

- import the depends module from fastapi

```
from fastapi import FastAPI, HTTPException, Depends
```

- changing get route to display the books from the database session

```
@app.get("/")

async def list_books(db: Session = Depends(get_db)):

    return db.query(model.Books).all()
```

- since we havent inputted any data, we update the post routes as well

```
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
```

- after this we can open swagger ui and execute the post and get route
- now we change the update route, change the data type of book_id to int and remove id: uuid from Book because we created the id column in the database of type int, so we dont need it anymore. it auto increments thanks to index = true

```
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
```

- finally we change the delete route as well, change the type of book_id

```
@app.delete("/delete_book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(model.Books).filter(
        model.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID : {book_id} does not exist"
        )
    db.query(model.Books).filter(model.Books.id == book_id).delete()
    db.commit()
```
