import httpx
from bot.config import bot_settings

class APIClient():
    def __init__(self):
        self.base_url = bot_settings.API_BASE_URL