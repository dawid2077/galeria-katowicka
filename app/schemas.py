#schemas.py
from pydantic import BaseModel,NonNegativeInt,Field
from pydantic_settings import BaseSettings
from typing import Optional,List,Literal
import uuid
from uuid_extension import uuid7
from datetime import datetime
from pydantic import EmailStr,ConfigDict



class chatMessage(BaseModel):
    role: Literal["user","assistant","system"]
    content: str = Field(
    min_length=1,
    max_length=10000,
    description="The prompt that will be sent to the Ai",
    examples=[
        "Powiedz mi o Muzeum Śląskie i Strefa Kultury gdzie sie znajduje co tam znajde ",
        ]
    )
class ChatHistory(BaseModel):
    conversation: List[chatMessage]


class UserCreate(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid7)
    email: EmailStr
    clerk_id=str

class UserResponse(BaseModel):
    user_id: uuid.UUID 
    email: EmailStr
    clerk_id: str
    created_at: datetime
    #to be honest i have no idea what this lines does only that it makes is so pydantic can work with sqlalchemy object rather than only a python dcit
    model_config: ConfigDict(from_attributes=True)
class SessionCreate(BaseModel):
    session_id: uuid.UUID
    chat_history=ChatHistory

class SessionRespose(BaseModel):
    session_id: uuid.UUID
    chat_history=ChatHistory
    created_at=datetime

class PlaceCreate(BaseModel):
    session_id: uuid.UUID
    name = str
    info = str
    location = str
class PlaceResponse(BaseModel):
    session_id: uuid.UUID
    name = str
    info = str
    location = str
