from django import forms
from .models import Partnership, PartnershipRequest, AcceptedPartnership


class PartnershipForm(forms.ModelForm):
    class Meta:
        model = Partnership
        fields = ['name', 'description', 'country']


class RequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['partnership', 'country']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = AcceptedPartnership
        fields = ['status', 'progress']