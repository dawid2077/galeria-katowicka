#main.py
from fastapi import FastAPI,HTTPException,status,Depends
from contextlib import asynccontextmanager
import os
import psycopg
import uuid


from typing import Optional
from uuid_extension import uuid7
from pydantic import Field


#from my files
from config import settings
from schemas import Book,BookNotFound,Message,BookUpdate 
from init import init_db
#this lacks rate limiting and can be targeted by ddos by sending big post requests (auth fixed it tho to some extent)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app=FastAPI(lifespan=lifespan)









