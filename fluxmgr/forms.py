from django import forms
from django.forms import TextInput


class DeployForm(forms.Form):
    version = forms.CharField(
        help_text="Flux version to deploy.",
        required=True,
        max_length=15
    )