from fastapi import FastAPI,HTTPException
import os
import psycopg
import uuid


from typing import Optional
from uuid_extension import uuid7
from pydantic import BaseModel, NonNegativeInt,Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These will automatically read from environment variables 
    # whether they come from a local .env file OR from Kubernetes!
    DATABASE_URL: str
    OPENAI_API_KEY: str
    VENUE_NAME: str = "Galeria Katowicka"

    # Updated to Pydantic V2 SettingsConfigDict syntax
    model_config = SettingsConfigDict(
        env_file="../configs/.env", 
        env_file_encoding="utf-8"
    )

# Instantiate the settings class so it loads the values from environment/.env
class Book(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid7)
    name:str
    author:str
    release_year:int
    quantity:NonNegativeInt
class BookUpdate(BaseModel):
    name: Optional[str]= None
    author: Optional[str]= None
    release_year: Optional[int]= None
    quantity: Optional[NonNegativeInt]= None

class Message(BaseModel):
    detail: str
settings =Settings()

app=FastAPI()


db: dict[uuid.UUID, Book] = {}
@app.get("/book")
def get_all_books() -> dict:
    return db
@app.get(
    "/book/{book_uuid}",
    responses={
        404: {
            "model": Message,
            "description": "Book not found"
        }
    }
    )
def get_book(book_uuid : uuid.UUID) -> dict:
    if book_uuid not in db:
        raise HTTPException(status_code=404,detail="Book not found")
    return db[book_uuid]
@app.post("/book")
def post_book(book : Book) -> dict:
    db[book.id]=book
    print("added sucessfully")
    return db[book.id]
@app.patch("/book/{book_uuid}")
def patch_book(book_uuid : uuid.UUID) -> None:
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
def delete_book(book_uuid: uuid.UUID) -> str:
    if book_uuid in db:
        del db[book_uuid]
    else:
        raise HTTPException(status_code=404,detail="Book not found")
    return f"deleted sucessfully"

