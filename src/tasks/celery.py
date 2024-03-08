# celery -A src.tasks worker --pool=solo
# https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying

from time import sleep

from celery import Celery
from config import REDIS_URL

celery = Celery("tasks", broker=REDIS_URL)
celery.conf.broker_connection_retry_on_startup = True


# bind=True to use self. conutdown overwrites default_retry_delay.
@celery.task(
    bind=True,
    default_retry_delay=30 * 60,
    max_retries=1,
)
def send_email(self, n):
    try:
        print("sending email..", n)
        sleep(10)
        # a = 1 / 0  # retry test
        print("email sent!", n)

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
