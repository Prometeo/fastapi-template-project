import getpass
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ValidationError, model_validator, ConfigDict, computed_field
from core.security import hash_password
from core.config import config
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Engine, text

engine: Engine = create_engine(config.DATABASE_URL)
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class UserModel(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)
    email: EmailStr
    first_name: str = Field(..., max_length=50, min_length=5, pattern=r"^[a-zA-Z]+$")
    last_name: str = Field(..., max_length=50, min_length=5, pattern=r"^[a-zA-Z]+$")
    username: str = Field(..., min_length=5, max_length=50, pattern=r"^[a-zA-Z]+$")
    password: str = Field(..., min_length=8)
    password_confirmation: str = Field(..., min_length=8)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserModel":
        if self.password != self.password_confirmation:
            raise ValueError("passwords do not match")
        return self

    @computed_field
    @property
    def hashed_password(self) -> str:
        return hash_password(self.password)


class User:
    def __init__(self, user_data: UserModel) -> None:
        self.user_data = user_data

    @staticmethod
    def set_user_data() -> UserModel | None:
        """
        Create and instance of UserModel with data provided by the user

        Returns:
            UserModel: A new instance of the UserModel class
        """
        username: str = input("Username: ")
        email: str = input("Email: ")
        first_name: str = input("First Name: ")
        last_name: str = input("Last Name: ")
        password: str = getpass.getpass("Password: ")
        password_confirmation: str = getpass.getpass("Confirm Password: ")
        try:
            user_model: UserModel = UserModel(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                password_confirmation=password_confirmation,
            )
            return user_model
        except ValidationError as e:
            print(e)
            return None

    def create(self) -> bool:
        """
        Creates a new user

        Returns:
            bool: True if success
        """

        sql = text("""
        INSERT INTO public.user (username, email, first_name, last_name, hashed_password, created_at, is_superuser, is_active, login_count, deleted)
        VALUES (:user, :email, :firstname, :lastname, :hashedpassword, :createdat, TRUE, TRUE, 0, FALSE)
        """)
        try:
            with engine.connect() as connection:
                connection.execute(
                    sql,
                    {
                        "user": self.user_data.username,
                        "email": self.user_data.email,
                        "firstname": self.user_data.first_name,
                        "lastname": self.user_data.last_name,
                        "hashedpassword": self.user_data.hashed_password,
                        "createdat": datetime.now(),
                    },
                )
                connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False


def main() -> None:
    user_data: UserModel | None = User.set_user_data()
    if user_data:
        super_user = User(user_data)
        super_user.create()
    else:
        print("Couldn't create the superuser")


if __name__ == "__main__":
    main()
