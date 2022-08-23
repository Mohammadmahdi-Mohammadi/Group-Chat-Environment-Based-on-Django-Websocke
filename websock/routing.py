from echo import routing as echo_routing
from chat import routing as chat_routing

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator



application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    echo_routing.websocket_urlpatterns +
                    chat_routing.websocket_urlpatterns
                )
            )
        )
    )
})
