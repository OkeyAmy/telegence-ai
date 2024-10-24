# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    TWILIO_ACCOUNT_SID: Optional[str]
    TWILIO_AUTH_TOKEN: Optional[str]
    SLACK_BOT_TOKEN: Optional[str]
    LINKEDIN_API_KEY: Optional[str]
    GOOGLE_CLIENT_SECRET: Optional[str]
    SLACK_APP_TOKEN: Optional[str]
    GOOGLE_CLIENT_IDD: Optional[str]

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()