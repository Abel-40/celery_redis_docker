from fastapi_mail import ConnectionConfig
from app.core.config import settings
from pathlib import Path

conf = ConnectionConfig(
  MAIL_USERNAME=settings.EMAIL,
  MAIL_PASSWORD=settings.MAIL_PASSWORD,
  MAIL_FROM=settings.EMAIL,
  MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
  MAIL_PORT=settings.MAIL_PORT,
  MAIL_SERVER=settings.MAIL_SERVER,
  MAIL_STARTTLS=True,
  MAIL_SSL_TLS=False,
  USE_CREDENTIALS=True,
  VALIDATE_CERTS=True,
  TEMPLATE_FOLDER=Path(__file__).parent / "templates",
  
)