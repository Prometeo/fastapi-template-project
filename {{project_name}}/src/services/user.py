from __future__ import annotations
from typing import TYPE_CHECKING
from crud.user import list_users, get_user_by_id, create_user, update_user, delete_user
from core.security import hash_password

if TYPE_CHECKING:
    from models.user import User
    from sqlalchemy.orm import Session
    from schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: Session) -> None:
        self._db = session

    def create_user(self, user_create: UserCreate) -> User:
        hashed_password: str = hash_password(user_create.password)
        return create_user(self._db, user_create, hashed_password)

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        return update_user(self._db, user_id, user_update)

    def delete_user(self, user_id: int) -> bool:
        return delete_user(self._db, user_id)

    def list_users(self) -> list[User]:
        return list_users(self._db)

    def get_user_by_id(self, user_id: int) -> User | None:
        return get_user_by_id(self._db, user_id)
