from django import forms
from .models import OurAgent, AgentImage

class OurAgentForm(forms.ModelForm):
    class Meta:
        model = OurAgent
        fields = ['names', 'portfolio', 'email', 'social_links', 'phone_number', 'bio', 'slug', 'active']

class AgentImageForm(forms.ModelForm):
    class Meta:
        model = AgentImage
        fields = ['image']
