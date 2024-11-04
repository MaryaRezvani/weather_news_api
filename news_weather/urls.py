from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeatherFormView.as_view(), name='weather_form'),
    path('api/weather-data/', views.WeatherDataAPI.as_view(), name='weather_data_api'),
    path('weather-display/', views.DisplayWeatherView.as_view(), name='weather_display'),
]

