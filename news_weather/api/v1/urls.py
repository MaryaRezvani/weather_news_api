from django.urls import path
from . import views

urlpatterns = [
    path('weather-data/', views.WeatherDataAPI.as_view(), name='weather_data_api'),
]


