from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import and_


def get_user(session: Session, username: str) -> User | None:
    return session.query(User).filter(and_(User.username == username.lower(), User.deleted.is_not(True))).first()
