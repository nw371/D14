from celery import shared_task
import time

from .views import collect_weekly_articles


@shared_task
def weekly_mails():
    collect_weekly_articles()
    print("EMAILS SENT")