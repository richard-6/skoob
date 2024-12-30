from fastapi import APIRouter, HTTPException

from app import schemas
from app.api.dependencies import CurrentActiveUserDep, SessionDep
from app.models import Role
from app.services import BookService, LoanService, UserService

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("/", response_model=schemas.Loan)
def create_loan(
    data: schemas.LoanCreate, session: SessionDep, current_user: CurrentActiveUserDep
):
    # TODO: Consider whether this validation would be better done in the service
    book_service = BookService(session=session)
    book = book_service.get_book_by_id(id=data.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No available copies")
    # Users should be able to self-serve or admins should be able to create loans for users
    if current_user.id != data.user_id and current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admins can create loans on behalf of other readers",
        )
    # TODO: Improve loan creation and update of book record to ensure the two stay in sync.
    # Currently we commit loan changes and update the book after.
    # Same thinking applies to functionality like updating the 'borrowed_books' field on the User model.
    loan = LoanService(session=session).create_loan(data=data)
    book_service.update_book(
        data=schemas.BookUpdate(id=book.id, available_copies=book.available_copies - 1)
    )
    user_service = UserService(session=session, current_user=current_user)
    user = user_service.get_user_by_id(id=data.user_id)
    if user:
        # FIXME: Pydantic/SQLALchemy model confusion here needs fixing.
        user_service.update_user(
            data=schemas.UserUpdate(
                id=user.id, borrowed_books=[*user.borrowed_books, book]
            )
        )
    return loan


@router.patch("/", response_model=schemas.Loan)
def update_loan(data: schemas.LoanUpdate, session: SessionDep, _: CurrentActiveUserDep):
    loan = LoanService(session=session).update_loan(data=data)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    book_service = BookService(session=session)
    book = book_service.get_book_by_id(id=loan.book_id)
    # If we have updated the loan then we shouldn't need to check if the book exists.
    # This needs refactoring.
    if book:
        book_service.update_book(
            data=schemas.BookUpdate(
                id=book.id, available_copies=book.available_copies + 1
            )
        )
    # TODO: Update borrowed_books field on User model when book is returned.
    return loan
