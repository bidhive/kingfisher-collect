from datetime import timedelta
from django.db.models import Q, QuerySet, Sum
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import status
from rest_framework.response import Response

from .models import Tender
from .serializers import TenderSerializer


class TenderViewSet(ModelViewSet):
    serializer_class = TenderSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Tender.objects.all()

    @action(detail=False, methods=["POST"])
    def search(self, request):
        query = request.data.get("query")
        tenders = self.get_queryset().filter(
            Q(name__icontains=query)
            | Q(country__icontains=query)
            | Q(publisher__name__icontains=query)
        )
        serializer = TenderSerializer(tenders, many=True)
        return Response(data=serializer.data)

    @action(detail=False, methods=["GET"])
    def countries(self, request):
        countries = dict((x, y) for x, y in Tender.country_choices)
        return Response(data=countries, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def metrics(self, request):
        total_count = Tender.objects.count()
        total_contract_value = Tender.objects.aggregate(Sum("contract_value"))[
            "contract_value__sum"
        ]
        data = {
            "total_count": total_count,
            "total_contract_value": total_contract_value,
        }
        return Response(data=data)

    @action(detail=False, methods=["GET"], url_path="todays-opportunities")
    def todays_opportunities(self, request):
        tenders = self.get_queryset().filter(
            publishedDate__gte=timezone.now() - timedelta(days=1)
        )
        serializer = TenderSerializer(tenders, many=True)
        return Response(serializer.data)
