from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.client import APIClient

router = Router()
api_client = APIClient()


class AddExpenseStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category_id = State()
    waiting_for_description = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    data = await api_client.login_telegram(telegram_id)
    access_token = data['access_token']
    await state.update_data(jwt_token=access_token)
    await message.answer(f'Hi! Token received. Your token: {access_token[:10]}. The token was saved.')


@router.message(Command('categories'))
async def cmd_get_categories(message: Message, state: FSMContext):
    user_data = await state.get_data()
    jwt_token = user_data.get('jwt_token')
    if not jwt_token:
        await message.answer(f'User is not authorized. Type \start and try again.')
        return
    categories = await api_client.get_categories(jwt_token)
    await message.answer(f'Your categories list: {categories}')


@router.message(Command('add_expense'))
async def add_expense(message: Message, state: FSMContext):
    pass