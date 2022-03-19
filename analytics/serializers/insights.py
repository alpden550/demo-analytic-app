from rest_framework import serializers


class InsightSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    channel = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    os = serializers.CharField(required=False)
    impressions = serializers.IntegerField(required=False)
    clicks = serializers.IntegerField(required=False)
    installs = serializers.IntegerField(required=False)
    spend = serializers.DecimalField(required=False, max_digits=20, decimal_places=2)
    revenue = serializers.DecimalField(required=False, max_digits=20, decimal_places=2)
    cpi = serializers.DecimalField(required=False, max_digits=20, decimal_places=2)
