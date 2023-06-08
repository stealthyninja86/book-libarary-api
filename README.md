# book-libarary-api

---

A book library API for cataloging books, allowing the user to perform operations like adding, retrieving, updating and deleting books using the FastAPI framework and book data is stored in SQLite DB.

# Getting Started

---

clone the repo onto your machine:

```
git clone https://github.com/stealthyninja86/book-libarary-api.git
```

install the required dependencies:

```
pip3 install -r requirements.txt
```

run the the fastAPI app

```
uvicorn main:app --reload
```
To access the swagger ui doc: http://127.0.0.1:8000/docs

Book library provide a Basic API Compose :

1. list all the books: http://127.0.0.1:8000/list_books

2. add a book: http://127.0.0.1:8000/add_book

3. updating book details: http://127.0.0.1:8000/update_book/{book_id}

4. deleting book: http://127.0.0.1:8000/delete_book/{book_id}
