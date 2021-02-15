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
    item = items[0]

    releases = item.pop("releases")
    release = releases[0]

    item_object = Tender.objects.create(**item)

    for key in release.keys():
        try:
            TenderRelease.objects.create(**release, item_id=item_object.id)
        except IntegrityError:
            continue

    shutil.rmtree(os.path.join("data"))
