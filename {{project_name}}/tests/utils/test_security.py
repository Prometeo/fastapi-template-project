import pytest
from core.security import verify_token, get_current_user, hash_password, create_access_token
from exceptions import UnauthorizedError
from crud.user import create_user
from schemas.user import UserCreate, UserResponse
from models.user import User


def test_verify_token() -> None:
    with pytest.raises(UnauthorizedError):
        verify_token("eiorrdsdksfdfklj82347")


async def test_get_current_user(db_test_session, user_test: UserCreate) -> None:
    user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    token: str = create_access_token({"username": user.username})
    current_user = await get_current_user(db_test_session, token)
    assert current_user
    assert isinstance(current_user, UserResponse)


async def test_invalid_current_user(db_test_session) -> None:
    with pytest.raises(UnauthorizedError):
        await get_current_user(db_test_session, "34iowioerio90")
