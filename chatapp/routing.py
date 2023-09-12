from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/some_path/$', consumers.WebSocketConsumer.as_asgi()),
    # Add more WebSocket URL patterns here if needed
]
