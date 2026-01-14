from pydantic import BaseModel


class BaseToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseToken):
    pass


class UserTokenResponse(BaseToken):
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
