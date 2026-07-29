from fastapi import APIRouter, Depends, status
from app.database import AsyncSession, get_async_session
from app.schemas import ExpenseCreate, ExpenseResponse
from app.security import get_current_user
from app.models import Expense, User

router = APIRouter(prefix='/expenses', tags=['Expenses'])


@router.post('/', response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(expense_data: ExpenseCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    new_expense = Expense(amount = expense_data.amount, currency = expense_data.currency, description = expense_data.description, category_id = expense_data.category_id, user_id = current_user.id)
    session.add(new_expense)
    await session.commit()
    await session.refresh(new_expense)
    return new_expense