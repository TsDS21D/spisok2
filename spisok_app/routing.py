from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/names/$', consumers.NamesConsumer.as_asgi()),
]