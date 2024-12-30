from fastapi import APIRouter

from app.api.routers import books, loans, login, users

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(books.router)
api_router.include_router(loans.router)
