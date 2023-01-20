import os

from celery import Celery

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

celery_app = Celery(
    "main",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.celery_app.tasks"],
)

celery_app.conf.update(
    event_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle", "json"],
)
