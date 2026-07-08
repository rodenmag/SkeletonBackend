from django.urls import re_path
from File.consumers import *

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    #re_path(r"ws/gemini/(?P<room_name>\w+)/$", GeminiConsumer.as_asgi()),
    re_path(r"ws/gemini/$", GeminiConsumer.as_asgi()),
]