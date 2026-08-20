#crud.py
from sqlalchemy.orm import Session,select,delete
from sqlalchemy import insert
import uuid
from schemas import Book,Author
from models import Author_table,Book_table
import structlog

logger = structlog.get_logger()
class CRUD:
    
    @staticmethod
    def get_by_id(db: Session,book_id : uuid.UUID) -> Book | None:
        book= db.get(Book, book_id)
        return book
    @staticmethod
    def get_author_by_id(db: Session,author_id: uuid.UUID) -> Author | None:
        author= db.get(Author, author_id)
        return author
    @staticmethod
    def get_all_books(db: Session) -> list[Book_table] | None:
        stmt = select(Book_table)
        books=db.scalars(stmt).all()
        #we check if len(0) to see if its empty
        if len(books)==0:
            return None
        else:
            return books
    @staticmethod
    def delete_book(db: Session,book_id : uuid.UUID)-> True | False:
        book= db.get(Book_table, book_id)
        if not book:
            return False
        db.delete(book)
        db.commit()
        return True
    @staticmethod
    def post_book(db : Session,new_book : Book,book_author : Author) -> None:
        author=CRUD.get_author_by_id(db,book_author.id)
        if author is None:
            db.add(book_author)
            db.flush()
            author=book_author
            new_book.author_id=author.id
        db.add(author)
        db.commit()
        return None



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