#models.py
#create the tables
from datetime import datetime
from typing import List, Any
from sqlalchemy import String, Uuid, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from pydantic import EmailStr
import uuid


class Base(DeclarativeBase):
    pass
class UserModel(Base):
    __tablename__="users"
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )
    email: Mapped[str]=mapped_column(String)
    clerk_id: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
class SessionModel(Base):
    __tablename__="sessions"
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )  
    session_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.user_id"), index=True
    )
    chat_history: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        default=list
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
        )
    #in future there will be last interacted column


class PlaceModel(Base):
    __tablename__="places"  
    place_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )  
    name: Mapped[str]=mapped_column(String)
    info: Mapped[str]=mapped_column(String)
    location: Mapped[str]=mapped_column(String)
    #in future will use postgres location amybe