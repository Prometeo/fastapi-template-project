from __future__ import annotations
from typing import TYPE_CHECKING
from core.security import authenticate_user, create_access_token

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from models.user import User


class AUTHService:
    def __init__(self, session: Session) -> None:
        self._db = session

    def authenticate(self, username: str, password: str) -> dict | None:
        user: User | None = authenticate_user(self._db, username, password)
        if not user:
            return None
        token: str = create_access_token({"username": user.username})
        return {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "access_token": token,
        }
