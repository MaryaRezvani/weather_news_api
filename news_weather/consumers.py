from channels.generic.websocket import AsyncWebsocketConsumer
import json
import hashlib

def get_city_hash(city_name):
    return hashlib.md5(city_name.encode('utf-8')).hexdigest()

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.city_name = self.scope['url_route']['kwargs']['city']
        self.city_hash = get_city_hash(self.city_name)
        self.room_group_name = f"weather_{self.city_hash}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'message' in text_data_json:
            message = text_data_json['message']

            # بررسی وجود کلیدها
            if 'temperature' in message and 'windspeed' in message:
                new_temperature = message['temperature']
                new_windspeed = message['windspeed']
                current_timestamp = message.get('timestamp', 'unknown')

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {       
                        'type': 'weather_update',
                        'message': {
                            'temperature': new_temperature,
                            'windspeed': new_windspeed,
                            'timestamp': current_timestamp
                        }           
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Missing temperature or windspeed in the message.'
                }))
        else:
            await self.send(text_data=json.dumps({
                'error': 'No message key found in the data received.'
            }))


    async def weather_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': {  # مطمئن شوید که داده‌ها به درستی در یک کلید message قرار گرفته‌اند
                'city': self.city_name,
                'temperature': message['temperature'],
                'windspeed': message['windspeed'],
                'timestamp': message['timestamp']
            }
        }))


