from rest_framework.serializers import ModelSerializer, JSONField

from .models import Tender, TenderRelease


class TenderReleaseSerializer(ModelSerializer):
    fields = JSONField()
    planning = JSONField()
    tender = JSONField()
    awards = JSONField()
    contract = JSONField()

    class Meta:
        model = TenderRelease
        fields = ("fields", "planning", "tender", "awards", "contract")


class TenderSerializer(ModelSerializer):
    publisher = JSONField()
    extensions = JSONField()
    links = JSONField()

    class Meta:
        model = Tender
        fields = (
            "uri",
            "publisher",
            "publishedDate",
            "licence",
            "version",
            "extensions",
            "links",
        )
