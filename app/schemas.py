import uuid
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid_extension import uuid7


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(
        min_length=1,
        max_length=10000,
        description="The prompt that will be sent to the AI",
        examples=[
            "Powiedz mi o Muzeum Śląskim i Strefie Kultury - gdzie się znajduje, co tam znajdę?",
        ],
    )


class ChatHistory(BaseModel):
    conversation: List[ChatMessage]


class UserCreate(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid7)
    email: EmailStr
    clerk_id: str


class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    clerk_id: str
    created_at: datetime
    #to be honest i have no idea what this lines does only that it makes is 
    # so pydantic can work with sqlalchemy object rather than only a python dict
    model_config = ConfigDict(from_attributes=True)


class SessionCreate(BaseModel):
    session_id: uuid.UUID = Field(default_factory=uuid7)
    chat_history: ChatHistory


class SessionResponse(BaseModel):
    session_id: uuid.UUID
    chat_history: ChatHistory
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlaceCreate(BaseModel):
    session_id: uuid.UUID
    name: str
    info: str
    location: str


class PlaceResponse(BaseModel):
    session_id: uuid.UUID
    name: str
    info: str
    location: str

    model_config = ConfigDict(from_attributes=True)