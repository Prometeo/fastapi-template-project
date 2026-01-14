from __future__ import annotations
from typing import Any
from fastapi import Depends
from fastapi import APIRouter
from services.auth import AUTHService
from schemas.auth import UserTokenResponse
from db.database import DbSession
from fastapi.security import OAuth2PasswordRequestForm
from exceptions import AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: DbSession) -> AUTHService:  # pragma: no cover
    return AUTHService(db)


@router.post("/login", response_model=UserTokenResponse)
def login(service: AUTHService = Depends(get_auth_service), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user: dict | None = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise AuthenticationError()
    return user
