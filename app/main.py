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
# 
from init import init_db
from routes import router as main_router
#this lacks rate limiting and can be targeted by ddos by sending big post requests (auth fixed it tho to some extent)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app=FastAPI(
    title="FastAPI Backend",
    lifespan=lifespan,
    version="0.1.0"
    )



#* this is so routes.py work
app.include_router(main_router)









