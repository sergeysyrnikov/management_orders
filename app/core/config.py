import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "dev")


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}",
        extra="ignore",
    )


settings = Settings()
