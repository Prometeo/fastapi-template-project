from __future__ import annotations
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Engine, text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.database import Base, get_db
from core.config import config
from schemas.user import UserCreate, UserResponse
from main import app
from core.security import get_current_user


DATABASE_URL: str = config.DATABASE_TEST_URL
engine: Engine = create_engine(DATABASE_URL)
TestingSessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_test_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def user_test() -> UserCreate:
    return UserCreate(
        username="test1234", email="test@gmail.com", first_name="test", last_name="test", password="testpassword"
    )


@pytest.fixture(scope="function", autouse=True)
def clean_data(db_test_session: Session) -> None:
    try:
        db_test_session.execute(text('TRUNCATE TABLE "user"'))
        db_test_session.commit()
    except Exception:
        db_test_session.rollback()
        raise


@pytest.fixture
def client(db_test_session: Session):
    """
    Overwrites the get_db dependency.
    """

    def override_get_db():
        try:
            yield db_test_session
        finally:
            pass  # Teardown is already handled by the db_test_session fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def authorized_client(client):
    def mock_get_current_user():
        return UserResponse(id=1001, username="testuser", first_name="Test", last_name="User", email="test@example.com")

    app.dependency_overrides[get_current_user] = mock_get_current_user

    yield client
    # Clean up without affecting other overrides (like db)
    app.dependency_overrides.pop(get_current_user, None)
