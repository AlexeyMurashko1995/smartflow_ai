from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.schemas import UserCreate, UserResponse, Token, UserTelegramAuth
from app.database import get_async_session, AsyncSession
from app.models import User
from app.security import get_password_hash, verify_password, create_access_token, get_current_user

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


@router.get('/me', response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/telegram-login', response_model=Token)
async def telegram_login(user_data: UserTelegramAuth, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.telegram_id==user_data.telegram_id)
    result = await session.execute(query)
    target_user = result.scalar_one_or_none()
    if target_user is None:
        target_user = User(telegram_id=user_data.telegram_id)
        session.add(target_user)
        await session.commit()
        await session.refresh(target_user)
    jwt_token = create_access_token(data={'sub': str(target_user.telegram_id)})
    return {'access_token': jwt_token, 'token_type': 'bearer'}