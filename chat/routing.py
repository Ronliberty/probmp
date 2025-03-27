from django.urls import re_path
from .consumers import GroupChatConsumer, P2PChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/group/(?P<group_id>\d+)/$', GroupChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<receiver_id>\d+)/$', P2PChatConsumer.as_asgi()),
]

