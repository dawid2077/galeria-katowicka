from fastapi import FastAPI,HTTPException,status,Depends
import os
import psycopg
import uuid


from typing import Optional
from uuid_extension import uuid7
from pydantic import Field


#from my files
from config import settings
from schemas import Book,BookNotFound,Message,BookUpdate

#this lacks rate limiting and can be targeted by ddos by sending big post requests (auth fixed it tho to some extent)


app=FastAPI()



class Database:

    def __init__(self) -> None:
        self.db={}
    def fetch_book(self,book_id)-> Book:
        if book_id not in self.db:
            raise BookNotFound(book_id)
        return self.db[book_id]
    def fetch_all_books(self) -> dict:
        return self.db
    def post_book(self,book: Book) -> None:
        self.db[book.id]=book
    def delete_book(self,book_id)->None:
        if book_id not in self.db:
            raise BookNotFound(book_id)
        del self.db[book_id]
        return None
    def patch_book() -> None:
        #here is the logic for patching but im too lazy to write it for now
        pass
database=Database()
def get_db_service():
    #here our class with a database that has connections (like postgres)
    try:
        yield database
    finally:
        pass



@app.get("/book")
def get_all_books(db: Database = Depends(get_db_service)) -> dict:
    return db.fetch_all_books()


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

