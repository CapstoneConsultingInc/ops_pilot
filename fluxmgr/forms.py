from django import forms
from django.forms import TextInput


class InstallForm(forms.Form):
    version = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Flux Version',
            'maxlength': '15',  # Adds maxlength attribute to the HTML input field
            'class': 'form-control',  # Adds Bootstrap styling to the input field
            'style': 'width: 300px;'  # Optional: controls the width of the input box
        })
    )
    
    cluster = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Cluster',
            'maxlength': '25',  # Adds maxlength attribute to the HTML input field
            'class': 'form-control',  # Adds Bootstrap styling to the input field
            'style': 'width: 300px;'  # Optional: controls the width of the input box
        })
    )
    
    required_css_class = "django_bootstrap5-req"
    
    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False