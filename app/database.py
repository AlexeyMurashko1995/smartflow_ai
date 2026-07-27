from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.config import settings


class Base(DeclarativeBase):
    pass


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session