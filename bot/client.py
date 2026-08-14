import httpx

from bot.config_bot import bot_settings


class APIClient:

    def __init__(self):
        self.base_url = bot_settings.API_BASE_URL

    async def login_telegram(self, telegram_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f'{self.base_url}/users/telegram-login',
                json={'telegram_id': telegram_id},
            )
            return response.json()

    async def get_categories(self, access_token: str):
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = await client.get(
                url=f'{self.base_url}/categories/',
                headers=headers,
            )
            return response.json()

    async def add_expense(
        self,
        access_token: str,
        amount: float,
        category_id: int,
        description: str | None = None,
    ):
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {access_token}'}
            payload = {'amount': amount, 'category_id': category_id, 'description': description}
            response = await client.post(
                url=f'{self.base_url}/expenses/',
                headers=headers,
                json=payload,
            )
            return response.json()

    async def get_expenses_summary(self, access_token: str):
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = await client.get(url=f'{self.base_url}/expenses/summary', headers=headers)
            return response.json()

    async def add_expense_via_ai(self, access_token: str, text: str):
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {access_token}'}
            payload = {'text': text}
            response = await client.post(url=f'{self.base_url}/expenses/ai', headers=headers, json=payload)
            return response.json()