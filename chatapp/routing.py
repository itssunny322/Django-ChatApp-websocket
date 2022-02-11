from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.conf.urls import url
from .consumer import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # url(r"^ws/consumer/", ChatConsumer),
            # path("ws/consumer/", ChatConsumer)
            url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
        ])
    ),

})