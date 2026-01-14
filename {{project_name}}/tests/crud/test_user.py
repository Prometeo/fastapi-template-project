from typing import TYPE_CHECKING
import pytest
from fastapi import HTTPException
from schemas.user import UserCreate, UserUpdate
from crud.user import create_user, list_users, get_user_by_id, update_user, delete_user
from core.security import hash_password

if TYPE_CHECKING:
    from models.user import User


def test_create_user(db_test_session, user_test) -> None:
    user = create_user(db_test_session, user_test, hash_password(user_test.password))
    assert user is not None
    assert user.email == user_test.email


def test_create_repeated_user(db_test_session, user_test) -> None:
    create_user(db_test_session, user_test, hash_password(user_test.password))
    with pytest.raises(HTTPException):
        create_user(db_test_session, user_test, hash_password(user_test.password))


def test_list_users(db_test_session, user_test: UserCreate) -> None:
    password = "test1234"
    user1 = create_user(db_test_session, user_test, hash_password(user_test.password))
    user_data = UserCreate(
        email="test2@gmail.com", first_name="test2", last_name="test2", password=password, username="123test"
    )
    user2 = create_user(db_test_session, user_data, hash_password(password))
    assert len(list_users(db_test_session)) == 2
    assert user1
    assert user2


def test_get_user_by_id(db_test_session, user_test: UserCreate) -> None:
    user = create_user(db_test_session, user_test, hash_password(user_test.password))
    user_retrieved = get_user_by_id(db_test_session, user.id)
    assert user_retrieved.username == user_test.username


def test_get_non_existent_user_by_id(db_test_session, user_test: UserCreate) -> None:
    create_user(db_test_session, user_test, hash_password(user_test.password))
    user_retrieved: User | None = get_user_by_id(db_test_session, 20)
    assert not user_retrieved


def test_update_user(db_test_session, user_test: UserCreate) -> None:
    user = create_user(db_test_session, user_test, hash_password(user_test.password))
    email = "test2@gmail.com"
    first_name = "test2"
    last_name = "test2"
    user_data = UserUpdate(email=email, first_name=first_name, last_name=last_name)
    updated_user = update_user(db_test_session, user.id, user_data)
    assert updated_user
    assert updated_user.email == email
    assert updated_user.first_name == first_name
    assert updated_user.last_name == last_name


def test_update_non_existent_user(db_test_session, user_test: UserCreate) -> None:
    create_user(db_test_session, user_test, hash_password(user_test.password))
    email = "test2@gmail.com"
    first_name = "test2"
    last_name = "test2"
    user_data = UserUpdate(email=email, first_name=first_name, last_name=last_name)
    updated_user = update_user(db_test_session, 300, user_data)
    assert not updated_user


def test_delete_user(db_test_session, user_test: UserCreate) -> None:
    user = create_user(db_test_session, user_test, hash_password(user_test.password))
    deleted = delete_user(db_test_session, user.id)
    user_deleted = get_user_by_id(db_test_session, user.id)
    assert deleted
    assert user_deleted.deleted is True


def test_delete_non_existent_user(db_test_session, user_test: UserCreate) -> None:
    create_user(db_test_session, user_test, hash_password(user_test.password))
    deleted = delete_user(db_test_session, 200)
    assert not deleted
