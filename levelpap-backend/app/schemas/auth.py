from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None


class UserWithToken(BaseModel):
    user: UserResponse
    token: Token

