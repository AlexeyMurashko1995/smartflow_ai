from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    email: Optional[EmailStr] = None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserTelegramAuth(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
