from django import forms
from .models import OurAgent, AgentImage, Information, InformationImage, InformationVideo

class OurAgentForm(forms.ModelForm):
    class Meta:
        model = OurAgent
        fields = ['names', 'portfolio', 'email', 'social_links', 'phone_number', 'bio', 'active']

class AgentImageForm(forms.ModelForm):
    class Meta:
        model = AgentImage
        fields = ['image']


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['name', 'description']

class InformationImageForm(forms.ModelForm):
    class Meta:
        model = InformationImage
        fields = ['image', 'caption']

class InformationVideoForm(forms.ModelForm):
    class Meta:
        model = InformationVideo
        fields = ['video', 'title']