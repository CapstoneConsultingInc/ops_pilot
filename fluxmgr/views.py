from django.contrib import messages
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from .forms import InstallForm, DeleteForm
    
class GetParametersMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", None)
        context["size"] = self.request.GET.get("size", None)
        return context
    
class InstallView(GetParametersMixin, FormView):
    template_name = "fluxmgr/install.html"
    form_class = InstallForm
    
class DeleteView(GetParametersMixin, FormView):
    template_name = "fluxmgr/delete.html"
    form_class = DeleteForm