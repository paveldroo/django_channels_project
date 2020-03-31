from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
                ]
            )
        )
    )
})

# ws://domain/<username>
