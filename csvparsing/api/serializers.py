from api.models import Deal
from rest_framework import serializers


class DealsSerializer(serializers.Serializer):
    """Serializes top 5 most valuable customers."""

    response = serializers.SerializerMethodField()

    class Meta:
        fields = ['response']

    def get_response(self, obj):
        gems_list = []
        for data in obj:
            gems = set(Deal.objects.filter(
                customer=data['username']
            ).values_list('item', flat=True))
            for i in list(gems):
                gems_list.append(i)
            data['gems'] = list(gems)
        for data in obj:
            for gem in data['gems']:
                amount = gems_list.count(gem)
                if amount == 1:
                    data['gems'].remove(gem)
        return obj


class ImportCsvSerializer(serializers.Serializer):
    """Imports a .csv file."""

    file = serializers.FileField(allow_empty_file=False)

    class Meta:
        fields = ['file']
