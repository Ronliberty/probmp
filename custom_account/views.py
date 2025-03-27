from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from allauth.account.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import CustomUserSignupForm, CustomUserLoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from allauth.account.auth_backends import AuthenticationBackend
from allauth.account.utils import send_email_confirmation
from django.http import HttpResponseRedirect
from allauth.account.utils import complete_signup
from allauth.account.adapter import get_adapter




class RedirectAfterLoginView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user

        # Check user's group membership and redirect accordingly
        if user.groups.filter(name='default').exists():
            return redirect('dashboard:user_dashboard')
        elif user.groups.filter(name='manager').exists():
            return redirect('dashboard:manager-dashboard')
        elif user.groups.filter(name='agent').exists():
            return redirect('dashboard:agent-dashboard')
        elif user.is_superuser:
            return redirect('dashboard:super-dash')

        # Fallback
        return redirect('base:index')

class CustomUserSignupView(FormView):
    template_name = "account/signup.html"
    form_class = CustomUserSignupForm
    success_url = reverse_lazy("account_email_verification_sent")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False  # Prevent login until email is confirmed
        user.save()

        # Trigger Allauth's email confirmation process
        return complete_signup(
            self.request,
            user,
            self.get_success_url(),
            signal_kwargs={"user": user},
        )



# Login View
class CustomUserLoginView(LoginView):
    template_name = "custom_account/login.html"
    authentication_form = CustomUserLoginForm
    redirect_authenticated_user = True





class SettingsView(TemplateView):
    template_name = 'custom_account/settings.html'


class AccountView(TemplateView):
    template_name = 'custom_account/custom_account.html'

class ProfileView(TemplateView):
    template_name = 'custom_account/profile.html'


class HelpView(TemplateView):
    template_name = 'custom_account/help.html'


class PoliciesView(TemplateView):
    template_name = 'custom_account/policy.html'



class NotificationsView(TemplateView):
    template_name = 'custom_account/notify.html'