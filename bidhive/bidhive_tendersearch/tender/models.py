from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Tender(models.Model):
    uri = models.CharField(max_length=1024)
    publisher = models.JSONField()
    publishedDate = models.DateTimeField()
    license = models.CharField(max_length=1024)
    version = models.CharField(max_length=1024)
    extensions = models.JSONField(null=True)
    links = models.JSONField(null=True)

    class Meta:
        db_table = "bidhive_tendersearch_tender"


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

    item = models.ForeignKey(Tender, related_name="releases", on_delete=models.CASCADE)

    class Meta:
        db_table = "bidhive_tendersearch_tender_release"
