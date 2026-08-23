#crud.py
from sqlalchemy.orm import Session,select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from schemas import Book,Author
from models import Author_table,Book_table
import structlog

logger = structlog.get_logger()
class CRUD:
    #C
    @staticmethod
    async def post_book(db : AsyncSession,new_book : Book,book_author : Author) -> None:
        author =await db.get(Author_table, book_author.id)
        if author is None:

            db.add(book_author)
            await db.flush()
            author=book_author

        new_book.author_id=author.id
        db.add(new_book)
        await db.commit()
        return None
    #R
    @staticmethod
    async def get_by_id(db: AsyncSession,book_id : uuid.UUID) -> Book | None:
        book= await db.get(Book_table, book_id)
        return book
    @staticmethod
    async def get_author_by_id(db: AsyncSession,author_id: uuid.UUID) -> Author | None:
        author= await db.get(Author_table, author_id)
        return author
    @staticmethod
    async def get_all_books(db: AsyncSession) -> list[Book_table]:
        stmt = select(Book_table)
        result = await db.scalars(stmt)
        books=result.all()
        return books
    #E
    @staticmethod
    def patch_book(db : Session,book_id : uuid.UUID) -> False:
        #TODO here i would iplement it by im too lazy for it 
        return False
    #D
    @staticmethod
    def delete_book(db: Session,book_id : uuid.UUID)-> bool:
        book= db.get(Book_table, book_id)
        if not book:
            return False
        db.delete(book)
        db.commit()
        return True



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