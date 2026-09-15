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
class Users(Base):
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
