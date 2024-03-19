from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_API_KEY: str

    class Config:
        env_file = '.env'


