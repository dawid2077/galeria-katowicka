#models.py
#create the tables
from datetime import datetime
from typing import List
from sqlalchemy import String,Uuid,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase,relationship
from pydantic import email
import uuid


class Base(DeclarativeBase):
    pass
class UserModel(Base):
    __tablename__="users"
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )
    email: Mapped[str]=mapped_column(String)
    google_id: Mapped[str]=mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
class SessionModel(Base):
    __tablename__="sessions"
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )   
    chat_history=Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        defaults=list
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
        )

class PlaceModel(Base):
    __tablename__="sessions"  
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )  
    name: Mapped[str]=mapped_column(String)
    info: Mapped[str]=mapped_column(String)
    location: Mapped[str]=mapped_column(String)