import os
import subprocess
import shutil

from django.db.utils import IntegrityError
from bidhive_tendersearch.models import Tender, TenderRelease
from utils import read_dirs

DEFAULT_TENDER_COUNT = 10
DEFAULT_FROM_DATE = "2021-02-01"


def run(*args):
    if "scrape" in args:
        subprocess.call(
            f"scrapy crawl australia -a from_date={DEFAULT_FROM_DATE} -a sample={DEFAULT_TENDER_COUNT}",
            shell=True,
        )

    path = os.path.join("data", "australia_sample")
    items = read_dirs(path)

    for item in items:
        releases = item.pop("releases")
        item_object = Tender.objects.create(**item)
        for release in releases:
            try:
                TenderRelease.objects.create(**release, item=item_object)
            except IntegrityError:
                continue

    shutil.rmtree(os.path.join("data"))
