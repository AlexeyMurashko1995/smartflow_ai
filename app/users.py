from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.schemas import UserCreate, UserResponse, Token
from app.database import get_async_session, AsyncSession
from app.models import User
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post('/login', response_model=Token)
async def get_login(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='User not found')
    comparison = verify_password(user_data.password, user.hashed_password)
    if not comparison:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return {'access_token': create_access_token(data={'sub': user.email}), 'token_type': 'bearer'}

