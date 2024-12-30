from typing import Iterable, Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Role, User
from app.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: Session, current_user: Optional[User] = None):
        self.crud = UserCRUD(session=session)
        self.current_user = current_user

    def get_users(self) -> list[User]:
        roles = {Role.READER}
        if self.current_user and self.current_user.role == Role.ADMIN:
            roles.add(Role.ADMIN)
        return self.crud.get_users(roles=roles)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.crud.get_user_by_username(username=username)

    # TODO: Signatures should be better aligned.
    # For example, this method includes borrowed books, but the `by_username` method above does not.
    def get_user_by_id(self, id: int) -> Optional[User]:
        user = self.crud.get_user_by_id(id=id)
        if not user:
            return None
        # Initial draft of role-based permissions, where only admins can view other admin users
        if (
            self.current_user
            and self.current_user.role != Role.ADMIN
            and user.role == Role.ADMIN
        ):
            return None
        return user

    def create_user(self, data: UserCreate) -> User:
        hashed_password = self._get_password_hash(password=data.password)
        return self.crud.create_user(
            username=data.username,
            hashed_password=hashed_password,
            is_active=data.is_active,
            is_superuser=data.is_superuser,
            role=data.role,
        )

    def update_user(self, data: UserUpdate) -> Optional[User]:
        return self.crud.update_user(data=data)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(username=username)
        if not user:
            return None
        if not self._verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return None
        return user

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class UserCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self, roles: Iterable[Role]):
        stmt = select(User).where(User.role.in_(roles))
        return self.session.scalars(stmt).all()

    def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        return self.session.scalars(stmt).first()

    def get_user_by_id(self, id: int) -> Optional[User]:
        stmt = (
            select(User).options(joinedload(User.borrowed_books)).where(User.id == id)
        )
        return self.session.scalars(stmt).first()

    def create_user(
        self,
        username: str,
        hashed_password: str,
        is_active: bool,
        is_superuser: bool,
        role: Role,
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser,
            role=role,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user(self, data: UserUpdate) -> Optional[User]:
        user = self.get_user_by_id(id=data.id)
        if not user:
            return None
        user.borrowed_books = data.borrowed_books
        self.session.commit()
        self.session.refresh(user)
        return user
