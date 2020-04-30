from cov19diff.models import DailyCsv
from rest_framework import serializers

class DailyCsvSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailyCsv
        fields = ['day', 'data']
