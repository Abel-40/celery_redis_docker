from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    CELERY_BROKER: str
    CELERY_BACKEND: str
    
    class Config:
      env_file = BASE_DIR/".env"

settings = Settings()