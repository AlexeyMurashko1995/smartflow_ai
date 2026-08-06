from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.client import APIClient

router = Router()
api_client = APIClient()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    data = await api_client.login_telegram(telegram_id)
    access_token = data['access_token']
    await state.update_data(jwt_token=access_token)
    await message.answer(f'Hi! Token received. Your token: {access_token[:10]}. The token was saved.')


@router.message(Command('categories'))
async def cmd_get_categories(message: Message, state: FSMContext):
    pass