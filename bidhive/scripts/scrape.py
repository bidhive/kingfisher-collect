import os
import subprocess
import shutil
from datetime import datetime

from django.db.utils import IntegrityError
from bidhive_tendersearch.models import Tender, TenderRelease
from utils import read_dirs

DEFAULT_TENDER_COUNT = 200
DEFAULT_FROM_DATE = "2021-02-11"
DEFAULT_ZONE = "australia"

ZONES = [country[0] for country in Tender.country_choices]
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TIME_FORMAT_TZ = "%Y-%m-%d%zT%H:%M:%SZ"


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

            # Keep consistent cases
            item["published_date"] = item.pop("publishedDate", None)
            item["deadline_date"] = item.pop("deadlineDate", None)
            item["publication_policy"] = item.pop("publicationPolicy", None)

            item_object = Tender(country=zone, **item)
            contract_value = None
            contract_currency = None

            for release in releases:
                try:
                    contracts = release.get("contracts")
                    if contracts is not None:
                        for contract in contracts:
                            if "value" in contract:
                                value = contract.get("value")
                                if "amount" in value:
                                    if contract_value is None:
                                        contract_value = 0
                                    contract_value += int(
                                        value.get("amount").split(".")[0]
                                    )

                                contract_currency = value.get("currency")

                    # TenderRelease.objects.create(**release, item=item_object)
                except IntegrityError:
                    continue

            if len(releases) > 0:
                last_release = releases[len(releases) - 1]
                if "tender" in last_release:
                    tender = last_release.get("tender")
                    # Some releases have the title as a direct property, some have it under the tender property
                    item_object.name = last_release.get("title", tender.get("title"))
                    item_object.name = tender.get("title", None)
                    item_object.id = tender.get("id")

                    contract_period = tender.get("contractPeriod")
                    if contract_period is not None:
                        if "startDate" in contract_period:
                            start_date_str = contract_period.get("startDate")
                            start_date = datetime.strptime(
                                start_date_str,
                                TIME_FORMAT_TZ
                                if "+" in start_date_str
                                else TIME_FORMAT,
                            )
                            item_object.start_date = start_date
                        if "endDate" in contract_period:
                            end_date_str = contract_period.get("endDate")
                            end_date = datetime.strptime(
                                end_date_str,
                                TIME_FORMAT_TZ
                                if "+" in start_date_str
                                else TIME_FORMAT,
                            )
                            item_object.end_date = end_date

                    item_object.procuring_entity = tender.get("procuringEntity")
                    item_object.procurement_method = tender.get("procurementMethod")
                    item_object.procurement_method_details = tender.get(
                        "procurementMethodDetails", None
                    )
                    item_object.tenderers = tender.get("tenderers", None)

                item_object.contract_value = contract_value
                item_object.contract_currency = contract_currency

                item_object.tag = last_release.get("tag")
                item_object.parties = last_release.get("parties")
                item_object.awards = last_release.get("awards")
                item_object.contracts = last_release.get("contracts")
                item_object.planning = last_release.get("planning")
                item_object.buyer = last_release.get("buyer")
                item_object.description = last_release.get("description")
                item_object.save()

                if "title" in last_release:
                    last_release.pop("title")

                if "description" in last_release:
                    last_release.pop("description")
                TenderRelease.objects.create(**last_release, item=item_object)

    # shutil.rmtree(os.path.join("data"))
