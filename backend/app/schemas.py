from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt

from app.models import Role


class UserBase(BaseModel):
    username: str
    is_active: bool
    role: Role


class User(UserBase):
    id: int


class UserDetail(User):
    borrowed_books: list["Book"]


class UserCreate(UserBase):
    password: str
    is_superuser: bool


class UserUpdate(BaseModel):
    id: int
    borrowed_books: list["Book"]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class BookBase(BaseModel):
    author: str
    description: Optional[str] = None
    available_copies: NonNegativeInt


class Book(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    id: int
    available_copies: NonNegativeInt


class LoanBase(BaseModel):
    book_id: int
    user_id: int


class Loan(LoanBase):
    id: int
    loaned_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    id: int
    returned_at: datetime
