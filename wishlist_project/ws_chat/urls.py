from django.urls.conf import path

from ws_chat.consumers import WishConsumer

websocket_url_patterns = [
    path('ws/chat/wishes/<int:wish_id>', WishConsumer.as_asgi(), name='wish_chat'),
]
