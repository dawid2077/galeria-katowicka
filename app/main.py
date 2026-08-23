#main.py
from fastapi import FastAPI,HTTPException,status,Depends
import os
import psycopg
import uuid


from typing import Optional
from uuid_extension import uuid7
from pydantic import Field


#from my files
from config import settings
from schemas import Book,BookNotFound,Message,BookUpdate 

#this lacks rate limiting and can be targeted by ddos by sending big post requests (auth fixed it tho to some extent)


app=FastAPI()









