from fastapi import FastAPI

from app.api.main import api_router
from app.db import SessionLocal, create_db
from app.models import Role
from app.schemas import UserCreate
from app.services import UserService
from app.settings import get_settings

settings = get_settings()

app = FastAPI()


@app.on_event("startup")
def startup():
    # TODO: Tables should be created with Alembic migrations
    create_db()
    with SessionLocal() as session:
        # TODO: Implement better approach for seeding test data
        user_service = UserService(session=session)
        if not user_service.get_user_by_username(
            username=settings.FIRST_SUPERUSER_USERNAME
        ):
            user_service.create_user(
                data=UserCreate(
                    username=settings.FIRST_SUPERUSER_USERNAME,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_active=True,
                    is_superuser=True,
                    role=Role.ADMIN,
                )
            )
        test_readers = {"alice", "bob"}
        for reader in test_readers:
            if not user_service.get_user_by_username(username=reader):
                user_service.create_user(
                    data=UserCreate(
                        username=reader,
                        password="books",
                        is_active=True,
                        is_superuser=False,
                        role=Role.READER,
                    )
                )


app.include_router(api_router)
