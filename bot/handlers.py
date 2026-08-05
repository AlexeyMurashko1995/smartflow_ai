from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.client import APIClient

router = Router()
api_client = APIClient()


@router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    data = await api_client.login_telegram(telegram_id)
    await message.answer("Hi! Token received")