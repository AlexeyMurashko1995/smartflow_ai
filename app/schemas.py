from datetime import datetime
from decimal import Decimal
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


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class ExpenseCreate(BaseModel):
    amount: Decimal
    currency: str = 'PLN'
    description: Optional[str] = None
    category_id: Optional[int] = None


class ExpenseResponse(BaseModel):
    id: int
    amount: Decimal
    currency: str
    description: Optional[str]
    category_id: Optional[int]
    created_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)
