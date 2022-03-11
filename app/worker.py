import os
from celery import Celery

from .config import session, hostname, index


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="index_data")
def index_data(data):
    response = session.post(url=f"{hostname}{index}/_doc/", json=data)
    print(response.text)
    if response.ok:
        return True
    else:
        return False
