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
    tenderers = serializers.JSONField()
    parties = serializers.JSONField()
    awards = serializers.JSONField()
    contracts = serializers.JSONField()
    planning = serializers.JSONField()
    buyer = serializers.JSONField()

    class Meta:
        model = Tender
        fields = (
            "id",
            "name",
            "country",
            "uri",
            "publisher",
            "published_date",
            "license",
            "version",
            "extensions",
            "links",
            "latest_release",
            "procuring_entity",
            "procurement_method",
            "procurement_method_details",
            "tag",
            "parties",
            "awards",
            "contracts",
            "planning",
            "buyer",
            "tenderers",
        )

    def get_latest_release(self, instance: Tender):
        return TenderReleaseSerializer(instance.latest_release).data


class TenderNameSerializer(DisableCreateUpdateSerializer):
    publisher = serializers.JSONField()

    class Meta:
        model = Tender
        fields = ("id", "publiser")
