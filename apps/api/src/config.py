from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Varinaut API"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./varinaut.db"

    ai_model_name: str = ""
    ai_model_api_key: str = ""
    ai_model_api_url: str = ""
    x_api_key: str = ""
    x_api_secret: str = ""
    polymarket_api_key: str = ""
    google_api_key: str = ""
    google_cse_id: str = ""

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
