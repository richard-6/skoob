from fastapi import APIRouter, HTTPException

from app import schemas
from app.api.dependencies import CurrentActiveUserDep, SessionDep
from app.models import Role
from app.services import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[schemas.Book])
def get_books(session: SessionDep, _: CurrentActiveUserDep):
    return BookService(session=session).get_books()


@router.get("/{id}", response_model=schemas.Book)
def get_book_by_id(id: int, session: SessionDep, _: CurrentActiveUserDep):
    book = BookService(session=session).get_book_by_id(id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=schemas.Book)
def create_book(
    data: schemas.BookCreate, session: SessionDep, current_user: CurrentActiveUserDep
):
    # TODO: Consider whether it would be better to instantiate
    # services with the user and apply permissions at the service level
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="User not allowed to create books")
    return BookService(session=session).create_book(data=data)


@router.patch("/", response_model=schemas.Book)
def update_book(data: schemas.BookUpdate, session: SessionDep, _: CurrentActiveUserDep):
    return BookService(session=session).update_book(data=data)
