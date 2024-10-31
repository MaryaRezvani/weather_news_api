from django.urls import path
from . import views

urlpatterns = [
    path('weather-form/', views.WeatherFormView.as_view(), name='weather_form'),
    path('api/weather-data/', views.WeatherDataAPI.as_view(), name='weather_data_api'),  # پردازش داده‌های آب و هوا
    path('weather-display/', views.DisplayWeatherView.as_view(), name='weather_display'),  # اضافه کردن URL جدید
]

