#models.py
#create the tables
from typing import List
from sqlalchemy import String,Uuid,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase,relationship


import uuid


#database schema
class Base(DeclarativeBase):
    pass

class Author_table(Base):
    __tablename__ = "authors"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)


    books: Mapped[List["Book_table"]] = relationship(back_populates="author")
class Book_table(Base):
    __tablename__="books"
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )
    name: Mapped[str]=mapped_column(String)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id",ondelete="CASCADE"))
    release_year: Mapped[int]=mapped_column()
    quantity: Mapped[int]=mapped_column()
    author: Mapped["Author_table"] = relationship(back_populates="books")



#

'''
CREATE TABLE authors(
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    name TEXT NOT NULL ,
    surname TEXT NOT NULL
);
'''
'''
CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    name VARCHAR NOT NULL,
    author_id UUID REFERENCES authors(id) ON DELETE CASCADE,
    release_year INTEGER NOT NULL,
    quantity INTEGER NOT NULL

);
'''