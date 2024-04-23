
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chatsystem.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from utils.auth_token import JwtAuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),
    "wss": JwtAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),

})
