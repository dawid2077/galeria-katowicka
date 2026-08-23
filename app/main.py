#main.py
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





