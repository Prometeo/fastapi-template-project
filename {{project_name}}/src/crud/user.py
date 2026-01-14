from schemas.user import UserCreate, UserUpdate
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from core.logger import logger


def list_users(session: Session) -> list[User]:
    return session.query(User).filter(User.deleted.is_(False)).all()


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def create_user(session: Session, user_create: UserCreate, password: str) -> User:
    try:
        user: User = User(
            username=user_create.username.lower(),
            email=user_create.email.lower(),
            hashed_password=password,
            first_name=user_create.first_name.lower(),
            last_name=user_create.last_name.lower(),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError as e:
        session.rollback()
        logger.exception(str(e))
        if "unique constraint" in str(e):
            message = "Error: A record with this unique identifier already exists."
            raise HTTPException(status_code=409, detail=message)
        elif "foreign key constraint" in str(e):  # pragma: no cover
            message = "Error: Related record does not exist."
            raise HTTPException(status_code=409, detail=message)
        else:
            raise HTTPException(status_code=409, detail="An integrity error occurred.")  # pragma: no cover
    except SQLAlchemyError as e:  # pragma: no cover
        logger.exception(str(e))
        session.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    except Exception as e:  # pragma: no cover
        logger.exception(str(e))
        session.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> User | None:
    user: User | None = get_user_by_id(session, user_id)
    if not user:
        return None
    user.email = user_update.email
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user: User | None = get_user_by_id(session, user_id)
    if not user:
        return False
    user.deleted = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return True
