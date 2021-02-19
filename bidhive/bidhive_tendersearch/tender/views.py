from datetime import timedelta
from django.db.models import Q, QuerySet, Sum
from django.utils import timezone
from django_filters import rest_framework as df_filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .models import Tender
from .serializers import TenderSerializer
from .utils import DefaultPagination, SubstringSearchFilter


class TenderFilterSet(df_filters.FilterSet):
    class Meta:
        model = Tender
        fields = ("name", "country", "publisher__name")


# TODO(alec): Implement pagination
class TenderViewSet(ModelViewSet):
    serializer_class = TenderSerializer
    permission_classes = (AllowAny,)
    pagination_class = DefaultPagination
    filter_class = TenderFilterSet
    filter_backends = (
        SubstringSearchFilter,
        df_filters.DjangoFilterBackend,
        OrderingFilter,
    )
    search_fields = ("name", "country", "publisher__name")
    ordering_fields = ["id", "name", "published_date"]
    ordering = ["published_date"]

    def get_queryset(self):
        return Tender.objects.all()

    @action(detail=False, methods=["POST"])
    def search(self, request):
        query = request.data.get("query")
        tenders = self.get_queryset().filter(
            Q(name__icontains=query)
            | Q(country__iexact=query)
            | Q(publisher__name__icontains=query)
        )

        awards_query = self.get_queryset().filter(
            awards__len__gte=1, awards__contains=[{"suppliers": [{"name": query}]}]
        )
        parties_query = self.get_queryset().filter(
            parties__len__gte=1, parties__contains=[{"name": query}]
        )
        tenderers_query = self.get_queryset().filter(
            tenderers__len__gte=1, tenderers__contains=[{"name": query}]
        )
        tenders = tenders.union(awards_query, parties_query, tenderers_query)

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
            published_date__gte=timezone.now() - timedelta(days=1)
        )
        serializer = TenderSerializer(tenders, many=True)
        return Response(serializer.data)
