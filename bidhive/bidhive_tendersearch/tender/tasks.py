from celery import shared_task
from django.utils import timezone
from .scrape import perform_scrape


@shared_task
def scrape_todays_tenders(now=timezone.now()):
    """
    Removes saved content library nodes which are more than two weeks old
    """
    perform_scrape(
        now=now, today=True, scrape=True, purge_data=True, via_celery=True, sample=10
    )
