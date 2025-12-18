from django.urls import re_path
from . import consumers
from . import test_consumer

websocket_urlpatterns = [
    re_path(r'ws/test/$', test_consumer.TestConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<stakeholder_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

