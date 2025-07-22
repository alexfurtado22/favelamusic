import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# ✨ FINAL FIX: Import the static files handler from Django's contrib apps
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application

import app.routing  # Make sure this points to your app's routing.py

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# The application is now a ProtocolTypeRouter that checks the request type
application = ProtocolTypeRouter(
    {
        # For standard HTTP requests, use the ASGIStaticFilesHandler which wraps the main Django app.
        # This will correctly serve static files in development (when DEBUG=True).
        "http": ASGIStaticFilesHandler(get_asgi_application()),
        # For WebSocket requests, use an authentication stack and a URL router
        "websocket": AuthMiddlewareStack(
            URLRouter(
                # This points to the websocket_urlpatterns in your app/routing.py file
                app.routing.websocket_urlpatterns
            )
        ),
    }
)
