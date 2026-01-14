from fastapi.testclient import TestClient
from models.user import User
from crud.user import create_user, get_user_by_id
from core.security import hash_password
from schemas.user import UserCreate


def test_login_user(db_test_session, client: TestClient, user_test: UserCreate) -> None:
    _: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    form_data = {"username": user_test.username, "password": user_test.password}
    response = client.post(
        "/auth/login/",
        data=form_data,
    )
    data = response.json()
    assert response.status_code == 200
    assert data["access_token"]
    assert data["username"] == user_test.username


def test_login_non_existent__user(client: TestClient) -> None:
    form_data = {"username": "error", "password": "error"}
    response = client.post(
        "/auth/login/",
        data=form_data,
    )
    assert response.status_code == 401
