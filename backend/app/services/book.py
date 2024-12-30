from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Book
from app.schemas import BookCreate, BookUpdate


class BookService:
    def __init__(self, session: Session):
        self.crud = BookCRUD(session=session)

    # TODO: Implement filtering and pagination
    def get_books(self) -> list[Book]:
        return self.crud.get_books()

    def get_book_by_id(self, id: int) -> Optional[Book]:
        return self.crud.get_book_by_id(id=id)

    def create_book(self, data: BookCreate) -> Book:
        return self.crud.create_book(data=data)

    def update_book(self, data: BookUpdate) -> Optional[Book]:
        return self.crud.update_book(data=data)


class BookCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_books(self) -> list[Book]:
        return self.session.query(Book).all()

    def get_book_by_id(self, id: int) -> Optional[Book]:
        stmt = select(Book).where(Book.id == id)
        return self.session.scalars(stmt).first()

    def create_book(self, data: BookCreate) -> Book:
        book = Book(
            title=data.title,
            author=data.author,
            description=data.description,
            available_copies=data.available_copies,
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def update_book(self, data: BookUpdate) -> Optional[Book]:
        book = self.get_book_by_id(id=data.id)
        if not book:
            return None
        book.available_copies = data.available_copies
        self.session.commit()
        self.session.refresh(book)
        return book
