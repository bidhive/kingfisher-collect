from django.db import models


class Tender(models.Model):
    data = models.JSONField()

    class Meta:
        db_table = "bidhive_tendersearch_tender"

