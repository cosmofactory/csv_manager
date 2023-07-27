from api.models import Deal
from rest_framework import viewsets
from api.serializers import DealsSerializer, ImportCsvSerializer
import csv
from io import TextIOWrapper
from rest_framework.response import Response


class DealsViewSet(viewsets.ModelViewSet):
    """Deals viewset."""

    queryset = Deal.objects.all()
    serializer_class = DealsSerializer

    def create(self, request):
        """Imports .csv file."""
        serializer = ImportCsvSerializer(data=request.data)
        if serializer.is_valid():
            try:
                file = request.FILES['file']
                decoding = TextIOWrapper(file, encoding='utf-8', newline='')
                rows = csv.reader(decoding)
                next(rows)  #  skipping column-name line
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
                Deal.objects.bulk_create(creation_list)
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


