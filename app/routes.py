#routes.py
from database import AsyncSessionLocal,get_db,AsyncSession
from schemas import ChatHistory,Message
from authClerk import get_current_user_id
from crud import CRUD
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter,FastAPI,HTTPException,status,Depends
from ai import llm_call,full_response
import uuid




router = APIRouter()

@staticmethod
@router.post("/chat/stream",
summary="Stream Ai Response",
description="--")
#* this exist so the response in small chunks which makes it look faster and more responsive
async def stream_chat(chat_data: ChatHistory) -> EventSourceResponse:
    #! in prod change debug_print_response to llm_call
    return EventSourceResponse(full_response(chat_data))

@staticmethod
@router.get("/test/endpoint")
async def show_user_id(
    db : AsyncSession=Depends(get_db),
    user_payload: dict = Depends(get_current_user_id)
    ) -> dict:
    user_id: str | None = payload.get("sub")
    email: str | None = user_payload.get("email")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing user ID ('sub' claim)",
        )
    return {
        "user_id": user_id,
        "email": email
    } 

        