from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/room/<str:room_id>/', consumers.ChatConsumer),
    # path('ws/<str:room_name>/', consumers.ChatConsumer),
]