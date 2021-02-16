import os
import subprocess
import shutil

from django.db.utils import IntegrityError
from bidhive_tendersearch.models import Tender, TenderRelease
from utils import read_dirs

DEFAULT_TENDER_COUNT = 100
DEFAULT_FROM_DATE = "2021-02-01"
DEFAULT_ZONE = "australia"

ZONES = [country[0] for country in Tender.country_choices]


def run(*args):
    if "clean" in args:
        Tender.objects.all().delete()

    if "scrape" in args:
        for zone in ZONES:
            subprocess.call(
                f"scrapy crawl {zone} -a from_date={DEFAULT_FROM_DATE} -a sample={DEFAULT_TENDER_COUNT}",
                shell=True,
            )

    for zone in ZONES:
        path = zone + "_sample"
        print(f"Loading tenders for path: {path}")
        path = os.path.join("data", path)
        items = read_dirs(path)

        for item in items:
            releases = sorted(item.pop("releases"), key=lambda r: r.get("date"))
            item_object = Tender.objects.create(country=zone, **item)
            for release in releases:
                try:
                    TenderRelease.objects.create(**release, item=item_object)
                except IntegrityError:
                    continue

            if len(releases) > 0:
                last_release = releases[len(releases) - 1]
                if "tender" in last_release and "title" in last_release.get("tender"):
                    item_object.name = last_release.get("tender").get("title")
                    item_object.save()

    shutil.rmtree(os.path.join("data"))
