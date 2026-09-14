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
