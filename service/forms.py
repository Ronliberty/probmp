from django import forms
from .models import Service, ServiceRequest, ServiceResponse


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'country', 'sample_website']



class RequestServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_deleted=False),
        empty_label="Select a service",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = ServiceRequest
        fields = ['service', 'additional_details', 'country']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = ServiceResponse
        fields = ['service_request', 'status', 'description', 'link']

        def __init__(self, *args, **kwargs):
            self.service_request = kwargs.pop('service_request', None)
            super().__init__(*args, **kwargs)

