from api.models import Deal
from rest_framework import serializers
import csv
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


class DealsSerializer(serializers.ModelSerializer):
    """Serializes incoming .csv file."""

    class Meta:
        model = Deal
        fields = ['customer', 'item', 'total', 'quantity', 'date']


class ImportCsvSerializer(serializers.Serializer):
    """Imports a .csv file."""

    file = serializers.FileField(allow_empty_file=False)

    class Meta:
        fields = ['file']