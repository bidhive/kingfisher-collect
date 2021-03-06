from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Tender(models.Model):
    # NOTE(alec): Many of the JSONFields can be either a JSON object/array or a string
    # with no real way of telling which way when loading the scraped data

    country_choices = (
        ("australia", "Australia"),
        ("australia_nsw", "New South Wales"),
        # ("uk_contracts_finder", "United Kingdom"),
        # ("italy", "Italy"),
    )
    id = models.CharField(max_length=1024, primary_key=True)
    name = models.CharField(max_length=1024, null=True)
    uri = models.CharField(max_length=1024)
    # Where countries are sourced from via scrapy
    country = models.CharField(max_length=1024, null=True, choices=country_choices)
    contract_value = models.BigIntegerField(null=True)
    contract_currency = models.CharField(max_length=3, null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=1024, null=True)
    submission_method = models.JSONField(null=True)
    submission_method_details = models.TextField(null=True)
    address_for_lodgement = models.TextField(null=True)
    type = models.CharField(max_length=1024, null=True)

    publisher = models.JSONField()
    license = models.CharField(max_length=1024)
    version = models.CharField(max_length=1024)
    extensions = models.JSONField(null=True)
    links = models.JSONField(null=True)
    publication_policy = models.JSONField(null=True)

    published_date = models.DateTimeField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    deadline_date = models.DateTimeField(null=True)

    # { id: string; name: string; }
    customer = models.JSONField(null=True)
    procurement_method = models.CharField(max_length=1024, null=True)
    procurement_method_details = models.TextField(null=True)

    tag = ArrayField(models.CharField(max_length=1024, blank=True), default=list)
    parties = ArrayField(models.JSONField(), default=list, null=True)
    awards = ArrayField(models.JSONField(), default=list, null=True)
    contracts = ArrayField(models.JSONField(), default=list, null=True)
    planning = models.JSONField(null=True)
    buyer = models.JSONField(null=True)
    documents = models.JSONField(null=True)
    amendments = models.JSONField(null=True)

    # { id: string; name: string; address?: Address; identifier?: { legalName: string; } }[]
    tenderers = models.JSONField(null=True)

    class Meta:
        db_table = "bidhive_tendersearch_tender"

    @property
    def latest_release(self):
        return self.releases.order_by("date").last()


class TenderRelease(models.Model):
    id = models.CharField(max_length=1024, primary_key=True)
    ocid = models.CharField(max_length=1024, null=True)
    date = models.DateTimeField(default=timezone.now)
    initiationType = models.CharField(max_length=1024, null=True)
    tag = ArrayField(models.CharField(max_length=1024, blank=True), default=list)
    language = models.CharField(max_length=1024, null=True)

    parties = ArrayField(models.JSONField(), default=list)
    awards = ArrayField(models.JSONField(), default=list)
    contracts = ArrayField(models.JSONField(), default=list)
    planning = models.JSONField(null=True)
    tender = models.JSONField(null=True)
    buyer = models.JSONField(null=True)

    item = models.ForeignKey(Tender, related_name="releases", on_delete=models.CASCADE)

    class Meta:
        db_table = "bidhive_tendersearch_tender_release"
