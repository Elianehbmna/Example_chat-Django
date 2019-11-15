from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from chat_ws.consumers import ChatConsumer

websockets = URLRouter([
    path("chats/<slug:convo_id>/<slug:member1_id>/<slug:member2_id>", ChatConsumer),
])

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "websocket": AuthMiddlewareStack(websockets)
})
