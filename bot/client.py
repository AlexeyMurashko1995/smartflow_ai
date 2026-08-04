import httpx
from bot.config_bot import bot_settings

class APIClient():
    def __init__(self):
        self.base_url = bot_settings.API_BASE_URL
    async def login_telegram(self, telegram_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post( url=f'{self.base_url}/users/telegram-login', json={'telegram_id': telegram_id})
        return response.json()