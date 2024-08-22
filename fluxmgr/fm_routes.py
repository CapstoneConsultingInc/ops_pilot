from django.urls import path

from . import consumers

cluster_manager_websocket_urlpatterns = [
    path("ws/fluxmgr/deploy-flux/", consumers.CreateClusterConsumer.as_asgi()),
]