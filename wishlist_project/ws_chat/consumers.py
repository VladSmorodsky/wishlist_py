import json
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

User = get_user_model()


class WishConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            return await self.close()
        self.wish_id = self.scope['url_route']['kwargs']['wish_id']
        self.room_group_name = f'wish_{self.wish_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, text_data, bytes_data=None):
        message = text_data['message']
        if message is None:
            return
        channel_layer = get_channel_layer()
        await channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'username': self.scope['user'].username,
        })

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps(
            {'username': username, 'message': message, 'created_at': datetime.now().strftime('%H:%M %m %d, %Y')}))
