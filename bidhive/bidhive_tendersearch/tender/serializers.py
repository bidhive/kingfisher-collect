from rest_framework.serializers import ModelSerializer, JSONField

from .models import Tender, TenderRelease


class DisableCreateUpdateSerializer(ModelSerializer):
    def create(self):
        raise ValueError(
            f"Cannot create serialised instances of {self.__class__.__name__}"
        )

    def update(self):
        raise ValueError(
            f"Cannot update serialised instances of {self.__class__.__name__}"
        )


class TenderReleaseSerializer(DisableCreateUpdateSerializer):
    parties = JSONField()
    awards = JSONField()
    contracts = JSONField()
    planning = JSONField()
    tender = JSONField()

    class Meta:
        model = TenderRelease
        fields = (
            "id",
            "ocid",
            "date",
            "initiationType",
            "tag",
            "language",
            "parties",
            "awards",
            "contracts",
            "planning",
            "tender",
        )


class TenderSerializer(DisableCreateUpdateSerializer):
    publisher = JSONField()
    extensions = JSONField()
    links = JSONField()

    class Meta:
        model = Tender
        fields = (
            "id",
            "uri",
            "publisher",
            "publishedDate",
            "license",
            "version",
            "extensions",
            "links",
        )
