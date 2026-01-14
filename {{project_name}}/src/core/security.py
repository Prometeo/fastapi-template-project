from __future__ import annotations
from typing import Any, Annotated
from fastapi import Depends
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError
from core.config import config
from jose import jwt, JWTError
from crud.auth import get_user
from sqlalchemy.orm import Session
from models.user import User
from exceptions import UnauthorizedError
from schemas.user import UserResponse
from db.database import get_db


ph: PasswordHasher = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed: str) -> bool:
    return ph.verify(hashed, plain_password)


def create_access_token(data: dict, expires_minutes: int = config.ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode: dict[Any, Any] = data.copy()
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user: User | None = get_user(session, username)
    if user:
        try:
            verify_password(password, user.hashed_password)
        except InvalidHashError:  # pragma: no cover
            return None
        except Exception as e:  # pragma: no cover
            return None
    else:
        return None
    return user


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str | None = payload.get("username")
        if username is None:
            raise UnauthorizedError
        return username
    except JWTError:
        raise UnauthorizedError


async def get_current_user(session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Any:
    username: str = verify_token(token)
    user: User | None = get_user(session, username)
    if not user:
        raise UnauthorizedError

    return UserResponse(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )


CurrentUser: CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
