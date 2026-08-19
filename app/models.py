#create the tables

from sqlalchemy import List,String,Uuid,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase,relationship


import uuid
class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)


    books: Mapped[List["Book"]] = relationship(back_populates="author")
class Book(Base):
    __tablename__="books"
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,primary_key=True
    )
    name: Mapped[str]=mapped_column(String)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id",ondelete="CASCADE"))
    release_year: Mapped[int]=mapped_column()
    quantity: Mapped[int]=mapped_column()
    author: Mapped["Author"] = relationship(back_populates="books")
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
#?basic crud
'''
INSERT INTO authors (id,name,surname) VALUES (
    '01a016b3-7a75-7468-8b3d-36f2d0da835c','Johann Wolfgang','von Goethe');

INSERT INTO books (name,author_id,release_year,quantity) VALUES (
    'Faust','01a016b3-7a75-7468-8b3d-36f2d0da835c','1833','3'
);

DELETE FROM books WHERE id= '01a016b3-7a75-7468-8b3d-36f2d0da835c';


SELECT books.name AS book_title,authors.name AS author_name,authors.surname,books.release_year,books.quantity FROM books 
JOIN authors ON books.author_id = authors.id
WHERE books.id='01a016b7-2ab0-705e-a26f-676d1bc8ec72';


SELECT books.name AS book_title,authors.name As author_name,authors.surname,books.release_year,books.quantity FROM books 
JOIN authors ON  books.author_id=authors.id;


UPDATE books SET name='Faust',release_year= '1833',quantity='2' WHERE books.id='01a016b7-2ab0-705e-a26f-676d1bc8ec72';

--someone buys the book

UPDATE books SET quantity=quantity-1 WHERE books.id='01a016b7-2ab0-705e-a26f-676d1bc8ec72';
'''