from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PicPay Simplificado"
    environment: str = "development"
    database_url: str = "sqlite:///./picpay.db"
    authorization_url: str = "https://util.devi.tools/api/v2/authorize"
    notification_url: str = "https://util.devi.tools/api/v1/notify"
    http_timeout_seconds: float = 5.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
