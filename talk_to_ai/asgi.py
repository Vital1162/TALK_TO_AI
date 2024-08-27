"""
ASGI config for talk_to_ai project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import conversation_ai.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talk_to_ai.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            conversation_ai.routing.websocket_urlpatterns
        )
    )
})