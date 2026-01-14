from fastapi import HTTPException


class UserError(HTTPException):
    """Base exception for user related errors"""

    pass


class UserNotFoundError(UserError):
    def __init__(self, user_id: int | None = None) -> None:
        message: str = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)


class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(status_code=401, detail=message)


class UnauthorizedError(HTTPException):
    def __init__(self, message: str = "Could not Validate credentials") -> None:
        super().__init__(status_code=401, detail=message, headers={"WWW-Authenticate": "Bearer"})
