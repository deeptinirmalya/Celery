import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_REDIAS_URL"),
    include=["tasks"]
)