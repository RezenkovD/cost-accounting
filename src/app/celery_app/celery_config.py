import os

from celery import Celery

BACKEND = os.getenv("BACKEND")
BROKER = os.getenv("BROKER")

celery_app = Celery(
    "main",
    backend=BACKEND,
    broker=BROKER,
    include=["app.celery_app.tasks"],
)

celery_app.conf.update(
    event_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle", "json"],
)
