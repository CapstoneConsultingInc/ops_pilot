from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from .forms import DeployForm

class HomePageView(TemplateView):
    template_name = "fluxmgr/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class GetParametersMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", None)
        context["size"] = self.request.GET.get("size", None)
        return context
    
class DeployView(GetParametersMixin, FormView):
    template_name = "fluxmgr/deploy.html"
    form_class = DeployForm