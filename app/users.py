from fastapi import APIRouter, Depends
from app.schemas import UserCreate, UserResponse
from app.database import get_async_session, AsyncSession
from app.models import User

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=UserResponse)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(email=user_data.email, hashed_password=user_data.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
