"""
URL configuration for ops_pilot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from fluxmgr.views import (
    InstallView,
    DeleteView
)
from landing.views import (
landing_page_view
)

urlpatterns = [
    path("", landing_page_view, name="home"),
    path("install/", InstallView.as_view(), name="flux_install"),
    path("delete/", DeleteView.as_view(), name="flux_delete"),
]
