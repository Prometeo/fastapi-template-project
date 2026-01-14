from typing import Generator
from fastapi import Depends
from typing import Annotated
from sqlalchemy import create_engine, Engine
from core.config import config
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import sessionmaker


engine: Engine = create_engine(config.DATABASE_URL)
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


DbSession = Annotated[Session, Depends(get_db)]
