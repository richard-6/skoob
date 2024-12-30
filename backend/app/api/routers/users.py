from fastapi import APIRouter, HTTPException

from app import schemas
from app.api.dependencies import CurrentActiveUserDep, SessionDep
from app.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[schemas.User])
def get_users(session: SessionDep, current_user: CurrentActiveUserDep):
    return UserService(session=session, current_user=current_user).get_users()


@router.get("/{id}", response_model=schemas.UserDetail)
def get_user_by_id(id: int, session: SessionDep, current_user: CurrentActiveUserDep):
    user = UserService(session=session, current_user=current_user).get_user_by_id(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
