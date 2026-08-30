#schemas.py
from pydantic import BaseModel,NonNegativeInt,Field
from pydantic_settings import BaseSettings
from typing import Optional,List,Literal
import uuid
from uuid_extension import uuid7


class chatMessage(BaseModel):
    role: Literal["user","assistant","system"]
    content: str =Field(
    min_length=1,
    max_length=10000,
    description="The prompt that will be sent to the Ai",
    examples=[
        "Powiedz mi o Muzeum Śląskie i Strefa Kultury gdzie sie znajduje co tam znajde ",
        ]
    )
class ChatHistory(BaseModel):
    conversation: List[chatMessage]
class Book(BaseModel):
    model_config = {"from_attributes": True}   # Pydantic v2 way of doing orm_mode
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