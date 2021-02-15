from rest_framework.viewsets import ModelViewSet

from .models import Tender


class TenderViewSet(ModelViewSet):
    def get_queryset(self):
        return Tender.objects.all()

