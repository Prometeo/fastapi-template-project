from datetime import date, datetime
from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from db.database import Base


class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        CheckConstraint("char_length(hashed_password) >= 32", name="ck_password_min_length"),
        {"comment": "User accounts for application access"},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[date] = mapped_column(default=datetime.now())
    login_count: Mapped[int] = mapped_column(default=0)
    deleted: Mapped[bool] = mapped_column(default=False)

    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("failed simple email validation")
        return address

    def __repr__(self) -> str:
        return f"<User(username={self.username}, email={self.email})>"
