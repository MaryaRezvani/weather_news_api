from rest_framework import serializers
from .models import Weather

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    windspeed = serializers.FloatField()
    timestamp = serializers.DateTimeField()

    def create(self, validated_data):
        return Weather.objects.create(**validated_data)  # ایجاد یک شیء جدید از مدل Weather

