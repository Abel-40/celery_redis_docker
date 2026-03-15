from pydantic_settings import BaseSettings
from pathlib import Path
from fastapi_mail import ConnectionConfig
BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_URL:str
    CELERY_BROKER: str
    CELERY_BACKEND: str
    EMAIL:str
    MAIL_PASSWORD:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM_NAME:str
    class Config:
      env_file = BASE_DIR / ".env"
      extra = "ignore"

settings = Settings()



