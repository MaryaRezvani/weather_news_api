from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Weather
import logging
import hashlib

def get_city_hash(city_name):
    return hashlib.md5(city_name.encode('utf-8')).hexdigest()  # تولید hash

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Weather)
def weather_data_updated(sender, instance, **kwargs):
    try:
        channel_layer = get_channel_layer()
        city_hash = get_city_hash(instance.city)
        async_to_sync(channel_layer.group_send)(
                f"weather_{city_hash}",
                {
                    "type": "send_weather_update",
                    "data": {
                        "city": instance.city,
                        "temperature": instance.temperature,
                        "windspeed": instance.windspeed,
                        "timestamp": instance.timestamp.strftime("%b. %d, %Y")
                    }
                }
            )
    except Exception as e:
        logger.error(f"Error sending weather update: {e}")

