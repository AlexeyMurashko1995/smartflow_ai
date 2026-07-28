from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    hashed_password: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    categories: Mapped[list['Category']] = relationship(back_populates='user')
    expenses: Mapped[list['Expense']] = relationship(back_populates='user')



class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='categories')
    expenses: Mapped[list['Expense']] = relationship(back_populates='category')


class Expense(Base):
    __tablename__ = 'expenses'
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(default='PLN')
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))
    user: Mapped['User'] = relationship(back_populates='expenses')
    category: Mapped[Optional['Category']] = relationship(back_populates='expenses')