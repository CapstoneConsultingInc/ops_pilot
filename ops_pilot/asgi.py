import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from fluxmgr import fm_routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "captain_ops.settings")

# The Asynchronous Server Gateway Interface (ASGI) is a calling convention 
# for web servers to forward requests to asynchronous-capable Python programming 
# language frameworks, and applications. Initialize Django ASGI application 
# early to ensure the AppRegistry is populated before importing code that may import 
# ORM models.
django_asgi_app = get_asgi_application()

all_routes = fm_routes.cluster_manager_websocket_urlpatterns
    
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(all_routes))
        )
    }
)