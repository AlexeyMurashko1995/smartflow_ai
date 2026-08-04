import httpx
from bot.config_bot import bot_settings

class APIClient():
    def __init__(self):
        self.base_url = bot_settings.API_BASE_URL
    async def login_telegram(self, telegram_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(url=f'{self.base_url}/users/telegram-login', json={'telegram_id': telegram_id})
        return response.json()

    async def get_categories(self, access_token: str):
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = await client.get(url=f'{self.base_url}/categories/', headers=headers)
            return response.json()

    async def add_expense(self, access_token: str, amount: float, category_id: int, description: str = None):
        pass