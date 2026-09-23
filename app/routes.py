#routes.py
from database import AsyncSessionLocal,get_db,AsyncSession
from schemas import ChatHistory,Message
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter,FastAPI,HTTPException,status,Depends,Response
from ai import llm_call,full_response
import uuid
from authClerk import auth_user
from userMethods import UserModel


router = APIRouter()

@router.post("/chat/stream",
summary="Stream Ai Response",
description="--")
#* this exist so the response in small chunks which makes it look faster and more responsive
async def stream_chat(chat_data: ChatHistory) -> EventSourceResponse:
    #! in prod change debug_print_response to llm_call
    return EventSourceResponse(full_response(chat_data))


#!add email excation from auth will work on that 
"""
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
"""

@router.get("/test/endpoint")
async def show_user_id_email(
    user: UserModel = Depends(auth_user),
):
    # 'user' is already a fully authenticated & database-synced UserModel instance
    return {
        "user_id": user.user_id,
        "email": user.email,
        "clerk_id": user.clerk_id,
    }

@router.get("/health/live",status_code=status.HTTP_200_OK)
async def healthy(response: Response)-> dict:
    #this is here so services know to not cache this response
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return {"status": "up"}

async def check_db():

@router.get("/health/ready",status_code=status.HTTP_200_OK)
async def ready(response: Response)-> dic:
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    result= await asyncion.gather(check_db())