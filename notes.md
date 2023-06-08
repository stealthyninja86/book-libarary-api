
- create a basic app route


- run the app using the command

- this will generate a link to access your api - http://127.0.0.1:8000/

- create books variable to store the list of books

- create a post route to for the create_books() which is used to add new books to the BOOKS variable


- now we can go to the swagger docs using the link http://127.0.0.1:8000/docs and test our api
















- after this we can open swagger ui and execute the post and get route


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