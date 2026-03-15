from celery import Celery
from app.core.config import settings
from app.core.email_config import conf
import time  # Use standard time for sync tasks
import requests
from fastapi_mail import FastMail, MessageSchema, MessageType
import asyncio
from redis import Redis
# Name the app something distinct from the tasks
celery_app = Celery("worker", broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND)
redis_client_for_worker = Redis.from_url(settings.REDIS_URL,max_connections=8)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600, # Increased to 1 hour
    task_track_started=True
)


celery_app.conf.beat_schedule = {
    "fetch-btc-price-every-60-seconds": {
        "task": "app.worker.monitor_btc_price",
        "schedule": 60.0,  # Run every 60 seconds
        # Alternatively, use crontab(minute="*") for every minute
    },
}


@celery_app.task(bind=True)
def monitor_btc_price(self):
    """Fetches Bitcoin price and logs it."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data["bitcoin"]["usd"]
        redis_client_for_worker.set("btc:price:latest", price)
        redis_client_for_worker.lpush("btc:price:history", price)
        redis_client_for_worker.ltrim("btc:price:history", 0, 99)
        print(f"--- BEAT REPORT ---")
        print(f"BTC Current Price: ${price}")
        return f"Price ${price} recorded"
    except Exception as exc:
        print(f"API Failed, retrying...")
        raise self.retry(exc=exc, countdown=60)
    
    
    
@celery_app.task(
    bind=True,
    autoretry_for=(Exception,), 
    retry_backoff=True,
    retry_backoff_max=600,
    max_retries=5
) 
def send_email(self, email: str):

    async def send():

        message = MessageSchema(
            subject="Welcome to InsightStream",
            recipients=[email],
            template_body={"email": email},
            subtype=MessageType.html
        )

        fm = FastMail(conf)

        await fm.send_message(
            message,
            template_name="welcome.html"
        )

    asyncio.run(send())

    print(f"Task ID: {self.request.id}")
    print(f"Email sent successfully to: {email}")
    
    
