from rest_framework import serializers
from news_weather.models import Weather

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    windspeed = serializers.FloatField()
    timestamp = serializers.DateTimeField()

    def create(self, validated_data):
        return Weather.objects.create(**validated_data)