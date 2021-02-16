from rest_framework import serializers

from .models import Tender, TenderRelease


class DisableCreateUpdateSerializer(serializers.ModelSerializer):
    def create(self):
        raise ValueError(
            f"Cannot create serialised instances of {self.__class__.__name__}"
        )

    def update(self):
        raise ValueError(
            f"Cannot update serialised instances of {self.__class__.__name__}"
        )


class TenderReleaseSerializer(DisableCreateUpdateSerializer):
    parties = serializers.JSONField()
    awards = serializers.JSONField()
    contracts = serializers.JSONField()
    planning = serializers.JSONField()
    tender = serializers.JSONField()

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
    publisher = serializers.JSONField()
    extensions = serializers.JSONField()
    links = serializers.JSONField()
    latest_release = serializers.SerializerMethodField()

    class Meta:
        model = Tender
        fields = (
            "id",
            "country",
            "uri",
            "publisher",
            "publishedDate",
            "license",
            "version",
            "extensions",
            "links",
            "latest_release",
        )

    def get_latest_release(self, instance: Tender):
        return TenderReleaseSerializer(instance.latest_release).data


class TenderNameSerializer(DisableCreateUpdateSerializer):
    publisher = serializers.JSONField()

    class Meta:
        model = Tender
        fields = ("id", "publiser")
