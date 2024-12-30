from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Loan
from app.schemas import LoanCreate, LoanUpdate


class LoanService:
    def __init__(self, session: Session):
        self.crud = LoanCRUD(session=session)

    def create_loan(self, data: LoanCreate) -> Loan:
        return self.crud.create_loan(data=data)

    def update_loan(self, data: LoanUpdate) -> Optional[Loan]:
        return self.crud.update_loan(data=data)


class LoanCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_loan_by_id(self, id: int) -> Optional[Loan]:
        stmt = select(Loan).where(Loan.id == id)
        return self.session.scalars(stmt).first()

    def create_loan(self, data: LoanCreate) -> Loan:
        loan = Loan(book_id=data.book_id, user_id=data.user_id)
        self.session.add(loan)
        self.session.commit()
        self.session.refresh(loan)
        return loan

    def update_loan(self, data: LoanUpdate) -> Optional[Loan]:
        loan = self.get_loan_by_id(id=data.id)
        if not loan:
            return None
        loan.returned_at = data.returned_at
        self.session.commit()
        self.session.refresh(loan)
        return loan
