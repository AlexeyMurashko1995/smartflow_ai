from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_BASE_URL: str = 'http://127.0.0.1:8000'
    model_config = SettingsConfigDict(env_file='.env')

bot_settings = Settings()