import os
import subprocess
import shutil
from datetime import datetime

from django.db.utils import IntegrityError
from bidhive_tendersearch.models import Tender, TenderRelease
from utils import read_dirs

DEFAULT_TENDER_COUNT = 1000
DEFAULT_FROM_DATE = "2020-05-01"
DEFAULT_ZONE = "australia"

ZONES = [country[0] for country in Tender.country_choices]
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TIME_FORMAT_TZ = "%Y-%m-%d%zT%H:%M:%SZ"


def _process_tender(item: Tender, tender: dict, last_release: dict):
    # Some releases have the title as a direct property, some have it under the tender property
    item.name = last_release.get("title", tender.get("title"))
    item.id = tender.get("id")
    contract_period = tender.get("contractPeriod") or tender.get("tenderPeriod")
    if isinstance(contract_period, dict):
        start_date_str = contract_period.get("startDate")
        end_date_str = contract_period.get("endDate")
        if start_date_str is not None:
            start_date = datetime.strptime(
                start_date_str, TIME_FORMAT_TZ if "+" in start_date_str else TIME_FORMAT
            )
            item.start_date = start_date
        if end_date_str is not None:
            end_date = datetime.strptime(
                end_date_str, TIME_FORMAT_TZ if "+" in end_date_str else TIME_FORMAT
            )
            item.end_date = end_date

    item.customer = tender.get("procuringEntity")
    item.procurement_method = tender.get("procurementMethod")
    item.procurement_method_details = tender.get("procurementMethodDetails", None)
    item.tenderers = tender.get("tenderers", None)
    item.documents = tender.get("documents")
    item.amendments = tender.get("amendments")
    item.status = tender.get("status")
    item.description = tender.get("description")
    item.submission_method = tender.get("submissionMethod")
    item.submission_method_details = tender.get("submissionMethodDetails")
    item.address_for_lodgement = tender.get("addressForLodgement")
    item.type = tender.get("inheritanceType")


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
                except IntegrityError:
                    continue

            if len(releases) > 0:
                last_release = releases[len(releases) - 1]
                if "tender" in last_release:
                    _process_tender(
                        item_object, last_release.get("tender"), last_release
                    )

                item_object.contract_value = contract_value
                item_object.contract_currency = contract_currency

                item_object.tag = last_release.get("tag")
                item_object.parties = last_release.get("parties")
                item_object.awards = last_release.get("awards")
                item_object.contracts = last_release.get("contracts")
                item_object.planning = last_release.get("planning")
                item_object.buyer = last_release.get("buyer")

                if item_object.description is None:
                    item_object.description = last_release.get("description")

                item_object.save()

                # TenderRelease.objects.create(**last_release, item=item_object)

    # shutil.rmtree(os.path.join("data"))
