from django.db.models import Q, QuerySet
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Tender
from .serializers import TenderSerializer


class TenderViewSet(ModelViewSet):
    serializer_class = TenderSerializer

    def get_queryset(self):
        return Tender.objects.all()

    @action(detail=False, methods=["POST"])
    def search(self, request):
        query = request.data.get("query")
        tenders = self.get_queryset().filter(
            Q(name__icontains=query) | Q(publisher__name__icontains=query)
        )
        serializer = TenderSerializer(tenders, many=True)
        return Response(data=serializer.data)
