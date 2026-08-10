from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.client import APIClient

router = Router()
api_client = APIClient()


class AddExpenseStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category_id = State()
    waiting_for_description = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    user_data = await api_client.login_telegram(telegram_id)
    access_token = user_data.get('access_token')
    await state.update_data(jwt_token=access_token)
    await message.answer(f'The token was successfully saved. Your token: {access_token[:10]}')


@router.message(Command('categories'))
async def get_categories(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    jwt_token = data.get('jwt_token')
    if not jwt_token:
        await message.answer('User not authorized. Please enter /start')
        return
    categories = await api_client.get_categories(jwt_token)
    await message.answer(f'Your categories: {categories}')


@router.message(Command('add_expense'))
async def add_expense(message: Message, state: FSMContext) -> None:
    await state.set_state(AddExpenseStates.waiting_for_amount)
    await message.answer('Enter the amount: ')