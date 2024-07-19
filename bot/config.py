from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram.fsm.storage.redis import Redis


class Settings(BaseSettings):
    BOT_TOKEN: str

    OS: str
    PATH_TO_PROJECT_WINDOWS: str
    PATH_TO_PROJECT_UNIX: str

    REDIS_HOST: str

    URL: str

    NATS_HOST: str
    NATS_CONSUMER_SUBJECT: str
    NATS_STREAM: str
    NATS_DURABLE_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
redis = Redis(host=settings.REDIS_HOST)
