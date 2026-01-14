from models.user import User
from crud.auth import get_user
from crud.user import create_user, delete_user
from core.security import hash_password


def test_authenticate_user(db_test_session, user_test, clean_data) -> None:
    created_user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    retrieved_user: User | None = get_user(db_test_session, created_user.username)
    assert retrieved_user
    assert created_user.username == retrieved_user.username


def test_authenticate_non_existent_user(db_test_session, clean_data) -> None:
    retrieved_user: User | None = get_user(db_test_session, "testing")
    assert not retrieved_user


def test_authenticate_deleted_user(db_test_session, user_test, clean_data) -> None:
    created_user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    delete_user(db_test_session, created_user.id)
    retrieved_user: User | None = get_user(db_test_session, created_user.username)
    assert not retrieved_user
