from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.WeatherFormView.as_view(), name='weather_form'),
    path('api/v1/', include('news_weather.api.v1.urls')),

    path('weather-display/', views.DisplayWeatherView.as_view(), name='weather_display'),
]

