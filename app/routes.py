from database import AsyncSessionLocal,get_db,AsyncSession
from schemas import Book,Author,BookNotFound,Message
from crud import CRUD
from fastapi import APIRouter,FastAPI,HTTPException,status,Depends

import uuid




router = APIRouter()
@router.get("/book")
async def route_get_all_books(db: AsyncSession = Depends(get_db)) -> dict:
    return await CRUD.get_all_books(db)
@router.get(
    "/book/{book_uuid}",
    responses={
        404: {
            "model": Message,
            "description": "Book not found"
        }
    }
    )
async def route_get_book(book_uuid : uuid.UUID,db: AsyncSession = Depends(get_db)):
    return await CRUD.get_by_id(db,book_uuid)
@router.post("/book")
async def route_post_book(book : Book,author : Author,db: AsyncSession=Depends(get_db)) -> dict:
    return await CRUD.post_book(db,book,author)
@router.patch("/book/{book_uuid}")
async def route_patch_book(book_uuid : uuid.UUID,db: AsyncSession=Depends(get_db)) -> None:
    pass
    #here i would update it  but im to lazy to write it 
@router.delete(
    "/book/{book_uuid}",
    responses={
        404: {
            "model": Message,
            "description": "The book with the specified UUID was not found.",
        }
    }
)
async def delete_book(book_uuid: uuid.UUID,db: AsyncSession=Depends(get_db)) -> None:
    return await CRUD.delete_book(db,book_uuid)
