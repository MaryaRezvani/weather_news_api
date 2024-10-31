
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import CityForm
from .serializers import WeatherSerializer
from .models import Weather
from django.views.generic import View,ListView
from django.views.generic.edit import FormView
from .cities import cities
from .regions import regions
import requests



class WeatherFormView(FormView):
    template_name = 'weather_form.html'
    form_class = CityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = regions  # افزودن لیست استان‌ها به کانتکست
        return context

class WeatherDataAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        state = request.data.get('state')
        city = request.data.get('city')

        # چک کردن وجود شهر در دیکشنری cities
        coordinates = cities.get(city)
        if coordinates:
            lat = coordinates.get('latitude')
            lon = coordinates.get('longitude')
            if lat is None or lon is None:
                return Response({'error': 'Coordinates not found for the city'}, status=400)

            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(api_url)
            weather_data = response.json()

            # چک کردن وجود داده‌های آب و هوا
            if 'current_weather' in weather_data:
                temperature = weather_data['current_weather'].get('temperature')
                windspeed = weather_data['current_weather'].get('windspeed')

                # ذخیره داده در دیتابیس
                weather = Weather.objects.create(
                    city=city,
                    temperature=temperature,
                    windspeed=windspeed,
                )

                # سریالایز کردن داده و برگرداندن پاسخ
                serializer = WeatherSerializer(weather)
                return Response(serializer.data)

            else:
                return Response({'error': 'Weather data not available'}, status=404)

        return Response({'error': 'City not found'}, status=404)



class DisplayWeatherView(View):
    def get(self, request):
        city = request.GET.get('city')  # دریافت نام شهر از پارامترهای کوئری
        if city:
            weather_data = Weather.objects.filter(city=city).order_by('-timestamp')
        else:
            weather_data = Weather.objects.all().order_by('-timestamp')

        return render(request, 'weather_display.html', {'weather_data': weather_data, 'selected_city': city})







