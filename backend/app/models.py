from datetime import datetime, timedelta
from enum import StrEnum
from typing import Optional

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


user_books_association = Table(
    "user_books",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("book_id", Integer, ForeignKey("books.id")),
)


class Role(StrEnum):
    ADMIN = "admin"
    READER = "reader"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(Enum(Role))

    borrowed_books: Mapped[list["Book"]] = relationship(
        secondary=user_books_association, back_populates="borrowers"
    )
    loans: Mapped[list["Loan"]] = relationship(
        back_populates="user",
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    description: Mapped[Optional[str]]
    available_copies: Mapped[int] = mapped_column(default=1)

    borrowers: Mapped[list[User]] = relationship(
        secondary=user_books_association, back_populates="borrowed_books"
    )
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # TODO: Improve derivation of due date etc
    loaned_at: Mapped[datetime] = mapped_column(default=datetime.now())
    due_date: Mapped[datetime] = mapped_column(
        default=datetime.now() + timedelta(weeks=2)
    )
    returned_at: Mapped[Optional[datetime]]

    book: Mapped[Book] = relationship(back_populates="loans")
    user: Mapped[User] = relationship(back_populates="loans")
