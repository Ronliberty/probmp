from django import forms
from .models import HeroContent, Service, ContactSubmission, SocialLink
from django.utils.html import escape


class HeroContentForm(forms.ModelForm):
    class Meta:
        model = HeroContent
        fields = ['title', 'subtitle', 'cta_text', 'cta_link', 'is_active', 'name', 'description', 'explanation']

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')
        if is_active and HeroContent.objects.filter(is_active=True).exists():
            raise forms.ValidationError("Only one Hero Content can be active at a time.")
        return is_active


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "description", "icon_url", "features"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'message']

    def clean(self):
        cleaned_data = super().clean()
        # Escape all user input
        cleaned_data['name'] = escape(cleaned_data.get('name', ''))
        cleaned_data['message'] = escape(cleaned_data.get('message', ''))
        return cleaned_data


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'select select-bordered w-full',
                'hx-get': '/api/check-platform/',  # Optional for async validation
                'hx-trigger': 'change'
            }),
            'url': forms.URLInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'https://example.com/profile'
            })
        }
        help_texts = {
            'url': "Enter the full URL to your profile/page"
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        platform = self.cleaned_data.get('platform')

        # Add platform-specific validation if needed
        if platform == 'whatsapp' and 'wa.me' not in url:
            raise forms.ValidationError("WhatsApp links should use the wa.me format")

        return url

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom labels if needed
        self.fields['platform'].label = "Social Platform"
        self.fields['url'].label = "Profile URL"