from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import CategoryCreate, CategoryResponse
from app.database import get_async_session, AsyncSession
from app.models import Category, User
from app.security import get_current_user

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.post('/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    new_category = Category(name = category_data.name, user_id = current_user.id)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category