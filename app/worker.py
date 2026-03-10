from celery import Celery
from app.core.config import settings

celery_app = Celery("my_task",broker=settings.CELERY_BROKER,backend=settings.CELERY_BACKEND)

# app/worker.py

@celery_app.task(bind=True) 
def send_email(self, email: str):
    print(f"Task ID: {self.request.id}")
    print(f"email sent successfully to :::::=====> {email}")
