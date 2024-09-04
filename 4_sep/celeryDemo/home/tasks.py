from celery import shared_task
import time

@shared_task
def add(x, y):
    time.sleep(13)
    return x + y