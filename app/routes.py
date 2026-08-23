#local files
from main import app

from database import AsyncSessionLocal,get_db,AsyncSession
from schemas import Book,BookNotFound,Message
from crud import get_all_books
from fastapi import FastAPI,HTTPException,status,Depends


import uuid


@app.get("/book")
def get_all_books(db: AsyncSession = Depends(get_db)) -> dict:

    return db.fetch_all_books()


@app.get("/book")
def get_all(db Async: )

@app.get(
    "/book/{book_uuid}",
    responses={
        404: {
            "model": Message,
            "description": "Book not found"
        }
    }
    )
def get_book(book_uuid : uuid.UUID,db : Database=Depends(get_db_service)) -> Book:
    try:
        return db.fetch_book(book_uuid)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book not found",
        )
@app.post("/book")
def post_book(book : Book,db: Database=Depends(get_db_service)) -> dict:
    db.post_book(book)
    return {"status": "Book added successfully","book_uuid":book.id}
@app.patch("/book/{book_uuid}")
def patch_book(book_uuid : uuid.UUID,db: Database=Depends(get_db_service)) -> None:
    pass
    #here i would update it  but im to lazy to write it 
@app.delete(
    "/book/{book_uuid}",
    responses={
        404: {
            "model": Message,
            "description": "The book with the specified UUID was not found.",
        }
    }
)
def delete_book(book_uuid: uuid.UUID,db: Database=Depends(get_db_service)) -> None:
    try:
        return db.delete_book(book_uuid)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book not found"
        )