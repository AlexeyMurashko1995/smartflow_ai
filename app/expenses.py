from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy import select, func
from app.ai_service import extract_expense_from_text, transcribe_audio
from app.database import AsyncSession, get_async_session
from app.schemas import ExpenseCreate, ExpenseResponse, CategorySummaryResponse, TextExpenseCreate, CategoryCreate
from app.security import get_current_user
from app.models import Expense, User, Category
from app.redis_client import redis_client
import json

router = APIRouter(prefix='/expenses', tags=['Expenses'])


@router.post('/', response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(expense_data: ExpenseCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    new_expense = Expense(amount = expense_data.amount, currency = expense_data.currency, description = expense_data.description, category_id = expense_data.category_id, user_id = current_user.id)
    session.add(new_expense)
    await session.commit()
    await session.refresh(new_expense)
    cache_key = f"summary_expenses:{current_user.id}"
    await redis_client.delete(cache_key)
    return new_expense


@router.get('/summary', response_model=list[CategorySummaryResponse])
async def get_expenses_summary(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    cache_key = f"summary_expenses:{current_user.id}"
    cached = await redis_client.get(cache_key)
    if cached is not None:
        return json.loads(cached)
    query = select(Expense.category_id, Category.name.label('category_name'), func.sum(Expense.amount).label('total_amount')).join(Category).where(Expense.user_id == current_user.id).group_by(Expense.category_id, Category.name)
    result = await session.execute(query)
    summary_list = result.all()
    data_to_cache = [{"category_id": row.category_id, "category_name": row.category_name, "total_amount": float(row.total_amount)} for row in summary_list]
    await redis_client.set(cache_key, json.dumps(data_to_cache), ex=300)
    return summary_list


@router.post('/ai', response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense_via_ai(expense_data: TextExpenseCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    current_expense = await extract_expense_from_text(expense_data.text)
    query = select(Category).where(Category.name==current_expense.category_name, Category.user_id==current_user.id)
    result = await session.execute(query)
    current_category = result.scalar_one_or_none()
    if not current_category:
        new_category = Category(name=current_expense.category_name, user_id=current_user.id)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        await redis_client.delete(f"categories:{current_user.id}")
        current_category = new_category
    new_expense = Expense(amount=current_expense.amount, description=current_expense.description, category_id=current_category.id, user_id=current_user.id)
    session.add(new_expense)
    await session.commit()
    await session.refresh(new_expense)
    cache_key = f"summary_expenses:{current_user.id}"
    await redis_client.delete(cache_key)
    return new_expense


@router.post('/ai_voice', response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense_voice_message(session: AsyncSession = Depends(get_async_session), file: UploadFile = File(), current_user: User = Depends(get_current_user)):
    text_bytes = await file.read()
    text = await transcribe_audio(text_bytes)
    current_expense = await extract_expense_from_text(text)
    query = select(Category).where(Category.name==current_expense.category_name, Category.user_id==current_user.id)
    result = await session.execute(query)
    current_category = result.scalar_one_or_none()
    if not current_category:
        new_category = Category(name=current_expense.category_name, user_id=current_user.id)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        await redis_client.delete(f"categories:{current_user.id}")
        current_category = new_category
    new_expense = Expense(amount=current_expense.amount, description=current_expense.description, category_id=current_category.id, user_id=current_user.id)
    session.add(new_expense)
    await session.commit()
    await session.refresh(new_expense)
    cache_key = f"summary_expenses:{current_user.id}"
    await redis_client.delete(cache_key)
    return new_expense
