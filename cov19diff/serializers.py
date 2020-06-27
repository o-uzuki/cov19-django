from cov19diff.models import DailyCsv
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

class DailyCsvSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailyCsv
        fields = ['day', 'data']

    def create(self, validated_data):
        try:
            csv = DailyCsv.objects.get(day=validated_data['day'])
            csv.delete()
        except ObjectDoesNotExist:
            pass
        dailycsv = DailyCsv(
            day = validated_data['day'],
            data = validated_data['data']
        )
        dailycsv.save()
        return dailycsv
