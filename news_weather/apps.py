from django.apps import AppConfig


class NewsWeatherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news_weather"

    def ready(self):
        import news_weather.signals
