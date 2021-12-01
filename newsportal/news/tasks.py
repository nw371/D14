from celery import shared_task

from .functions import collect_weekly_articles, notify_subscribers_publication


@shared_task
def weekly_mails():
    collect_weekly_articles()
    print("EMAILS SENT")

@shared_task
def article_created(oid):
    print(f"OID *********************************************************************** {oid}")
    notify_subscribers_publication(oid)