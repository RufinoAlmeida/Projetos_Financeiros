from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Finance System API"
    debug: bool = True
    database_url: str = "sqlite:///./finance.db"
    secret_key: str = "change-this-secret"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
