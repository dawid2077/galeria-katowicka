#routes.py
from database import AsyncSessionLocal,get_db,AsyncSession
from schemas import ChatHistory,Book,Author,BookNotFound,Message
from crud import CRUD
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter,FastAPI,HTTPException,status,Depends
from ai import llm_call,full_response
import uuid




router = APIRouter()
@router.post("/chat/stream",
summary="Stream Ai Response",
description="--")
#* this exist so the response in small chunks which makes it look faster and more responsive
async def stream_chat(chat_data: ChatHistory) -> EventSourceResponse:
    #! in prod change debug_print_response to llm_call
    return EventSourceResponse(full_response(chat_data))
