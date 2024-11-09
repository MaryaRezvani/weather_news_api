from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import CityForm
from .models import Weather
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from .cities import cities
from .regions import regions
import requests

class WeatherFormView(FormView):
    template_name = 'home.html'
    form_class = CityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = regions
        
        tehran_coordinates = cities.get("تهران")
        if tehran_coordinates:
            lat = tehran_coordinates.get('latitude')
            lon = tehran_coordinates.get('longitude')
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(api_url)

            if response.status_code == 200:
                weather_data = response.json()

                if 'current_weather' in weather_data:
                    context['tehran_weather'] = {
                        'temperature': weather_data['current_weather'].get('temperature'),
                        'windspeed': weather_data['current_weather'].get('windspeed')
                    }
                else:
                    context['tehran_weather'] = None
            else:
                context['tehran_weather'] = None
        
        return context

    def form_valid(self, form):
        # Handle form submission logic here if needed
        return redirect('weather_display')  # Adjust this to your URL pattern name


class DisplayWeatherView(View):
    def get(self, request):
        city = request.GET.get('city')
        if city:
            weather_data = Weather.objects.filter(city=city).order_by('-timestamp')
        else:
            weather_data = Weather.objects.all().order_by('-timestamp')

        return render(request, 'weather_display.html', {'weather_data': weather_data, 'selected_city': city})



