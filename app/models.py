from sqlalchemy import Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from typing import Optional

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    hashed_password: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)