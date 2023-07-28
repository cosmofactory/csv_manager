import csv
from io import TextIOWrapper

from api.models import Deal
from api.serializers import DealsSerializer, ImportCsvSerializer
from django.db import transaction
from django.db.models import Sum, F
from rest_framework import mixins, viewsets
from rest_framework.response import Response


CUSTOMER_LIMIT = 5


class DealsViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    """Deals viewset."""

    queryset = Deal.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ImportCsvSerializer
        return DealsSerializer

    @transaction.atomic
    def create(self, request):
        """Imports .csv file with deals information."""
        serializer = ImportCsvSerializer(data=request.data)
        if serializer.is_valid():
            try:
                file = request.FILES['file']
                decoding = TextIOWrapper(file, encoding='utf-8', newline='')
                rows = csv.reader(decoding)
                next(rows)  # skipping column-name line
                creation_list = []
                for row in (rows):
                    creation_list.append(
                        Deal(
                            customer=row[0],
                            item=row[1],
                            total=row[2],
                            quantity=row[3],
                            date=row[4]
                        )
                    )
                Deal.objects.bulk_create(creation_list, ignore_conflicts=True)
                return Response('Status: OK - файл был обработан без ошибок')
            except Exception as error:
                return Response(
                    f'Status: Error, Desc: {error}'
                    ' - в процессе обработки файла произошла ошибка.'
                )
        return Response(
            f'Status: Error, Desc: {serializer.errors}'
            ' - в процессе обработки файла произошла ошибка.'
            )

    def list(self, request):
        """
        Returns top 5 most valuable clients.

        The value of clients is determined by the total sum they've
        spent through all of the registered deals.
        """

        queryset = Deal.objects.annotate(
            username=F('customer')
        ).values('username').annotate(
            spent_money=Sum('total')
        ).order_by('-spent_money')[:CUSTOMER_LIMIT]
        serializer = DealsSerializer(queryset)
        return Response(serializer.data)
