from __future__ import annotations
from fastapi import APIRouter, Depends
from services.user import UserService
from schemas.user import UserResponse, UserCreate, UserUpdate
from db.database import DbSession
from exceptions import UserNotFoundError
from models.user import User
from core.security import CurrentUser


router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: DbSession) -> UserService:
    return UserService(db)


@router.get("/", response_model=list[UserResponse], status_code=200)
def get_users(current_user: CurrentUser, service: UserService = Depends(get_user_service)) -> list[User]:
    return service.list_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user_by_id(user_id: int, current_user: CurrentUser, service: UserService = Depends(get_user_service)) -> User:
    user: User | None = service.get_user_by_id(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    current_user: CurrentUser, user_in: UserCreate, service: UserService = Depends(get_user_service)
) -> User:
    return service.create_user(user_in)


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(
    user_id: int, user_in: UserUpdate, current_user: CurrentUser, service: UserService = Depends(get_user_service)
) -> User:
    user: User | None = service.update_user(user_id, user_in)
    if not user:
        raise UserNotFoundError(user_id)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, current_user: CurrentUser, service: UserService = Depends(get_user_service)) -> None:
    result: bool = service.delete_user(user_id)
    if not result:
        raise UserNotFoundError(user_id)
