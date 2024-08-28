from django.urls import path

from . import consumers

flux_manager_websocket_urlpatterns = [
    path("ws/fluxmgr/install-flux/", consumers.InstallFluxConsumer.as_asgi()),
    path("ws/fluxmgr/delete-flux/", consumers.DeleteFluxConsumer.as_asgi()),
]