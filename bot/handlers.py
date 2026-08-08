"""Router module for handling financial expenses and Telegram bot commands."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
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
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Handle /start command, authenticate user via Telegram ID, and store JWT token."""
    telegram_id = message.from_user.id
    data = await api_client.login_telegram(telegram_id)
    access_token = data["access_token"]
    await state.update_data(jwt_token=access_token)
    await message.answer(
        f"Hi! Token received. Your token: {access_token[:10]}. The token was saved."
    )


@router.message(Command("categories"))
async def cmd_get_categories(message: Message, state: FSMContext) -> None:
    """Fetch and display available categories for authorized users."""
    user_data = await state.get_data()
    jwt_token = user_data.get("jwt_token")
    if not jwt_token:
        await message.answer("User is not authorized. Type /start and try again.")
        return
    categories = await api_client.get_categories(jwt_token)
    await message.answer(f"Your categories list: {categories}")


@router.message(Command("add_expense"))
async def add_expense(message: Message, state: FSMContext) -> None:
    await state.set_state(AddExpenseStates.waiting_for_amount)
    await message.answer('Enter the amount: ')


@router.message(AddExpenseStates.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
        await state.update_data(amount=amount)
        await state.set_state(AddExpenseStates.waiting_for_category_id)
        await message.answer("Great! Now enter the category ID: ")
    except ValueError:
        await message.answer("Enter the correct amount: ")
        return


@router.message(AddExpenseStates.waiting_for_category_id)
async def process_category_id(message: Message, state: FSMContext) -> None:
    try:
        category_id = int(message.text)
        if category_id <= 0:
            raise ValueError
        await state.update_data(category_id=category_id)
        await state.set_state(AddExpenseStates.waiting_for_description)
        await message.answer("Nice! Please enter the description: ")
    except ValueError:
        await message.answer("Enter the correct category ID: ")
        return