from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def get_user_dashboard_url(user):
    if user.is_superuser:
        return reverse('dashboard:super-dash')
    elif user.groups.filter(name='manager').exists():
        return reverse('dashboard:manager-dashboard')
    elif user.groups.filter(name='agent').exists():
        return reverse('dashboard:agent-dashboard')
    return reverse('dashboard:user_dashboard')