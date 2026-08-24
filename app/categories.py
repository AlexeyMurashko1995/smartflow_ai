import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.schemas import CategoryCreate, CategoryResponse
from app.database import get_async_session, AsyncSession
from app.models import Category, User
from app.redis_client import redis_client
from app.security import get_current_user

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.post('/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    new_category = Category(name = category_data.name, user_id = current_user.id)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


@router.get('/', response_model=list[CategoryResponse])
async def get_all_categories(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    cache_key = f"categories:{current_user.id}"
    cached = await redis_client.get(cache_key)
    if cached is not None:
        return json.loads(cached)
    query = select(Category).where(current_user.id == Category.user_id)
    result = await session.execute(query)
    categories_list = result.scalars().all()
    data_to_cache = [{"id": c.id, "name": c.name} for c in categories_list]
    await redis_client.set(cache_key, json.dumps(data_to_cache), ex=300)
    return categories_list