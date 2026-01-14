from fastapi.testclient import TestClient
from models.user import User
from crud.user import create_user, get_user_by_id
from core.security import hash_password
from schemas.user import UserCreate


def test_create_user(client: TestClient, authorized_client) -> None:
    response = client.post(
        "/users/",
        json={
            "username": "usertest435",
            "email": "test@gmail.com",
            "first_name": "test",
            "last_name": "test",
            "password": "password",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "usertest435"
    assert data["email"] == "test@gmail.com"
    assert "id" in data


def test_get_user_by_id(db_test_session, user_test: UserCreate, client: TestClient, authorized_client) -> None:
    user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_test.username
    assert data["email"] == user_test.email
    assert "id" in data


def test_get_non_existent_user_by_id(client: TestClient, authorized_client) -> None:
    response = client.get("/users/3000")
    assert response.status_code == 404


def test_update_user(db_test_session, user_test: UserCreate, client: TestClient, authorized_client) -> None:
    user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    response = client.put(
        f"/users/{user.id}", json={"email": "testing@gmail.com", "first_name": "testing", "last_name": "testing"}
    )
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["email"] == "testing@gmail.com"
    assert data["first_name"] == "testing"
    assert data["last_name"] == "testing"
    assert "id" in data


def test_udapte_non_existent_user(client: TestClient, authorized_client) -> None:
    response = client.put(
        "/users/4000", json={"email": "testing@gmail.com", "first_name": "testing", "last_name": "testing"}
    )
    assert response.status_code == 404


def test_delete_user(db_test_session, user_test: UserCreate, client: TestClient, authorized_client) -> None:
    user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    response = client.delete(f"/users/{user.id}")
    deleted_user = get_user_by_id(db_test_session, user.id)
    assert response.status_code == 204
    assert deleted_user.deleted


def test_delete_non_existent_user(client: TestClient, authorized_client) -> None:
    response = client.delete("/users/3000")
    assert response.status_code == 404


def test_list_users(db_test_session, client: TestClient, user_test: UserCreate, authorized_client) -> None:
    user: User | None = create_user(db_test_session, user_test, hash_password(user_test.password))
    response = client.get("users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == user.username
    assert data[0]["email"] == user.email
