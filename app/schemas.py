#schemas.py
from pydantic import BaseModel,NonNegativeInt,Field
from pydantic_settings import Setting
from typing import Optional
import uuid
from uuid_extension import uuid7
class Book(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid7)
    name: str
    author_id: uuid.UUID 
    release_year: int
    quantity: NonNegativeInt
class Author(BaseModel):
    id : uuid.UUID = Field(default_factory=uuid7)
    name: str
    surname: str
class BookUpdate(BaseModel):
    name: Optional[str]= None
    author: Optional[str]= None
    release_year: Optional[int]= None
    quantity: Optional[NonNegativeInt]= None

class Message(BaseModel):
    detail: str

class BookNotFound(Exception):

    def __init__(self, book_id: str):
        self.book_id=book_id