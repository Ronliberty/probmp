from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from allauth.account.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import CustomUserSignupForm, CustomUserLoginForm, CustomUserCreateForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from django.http import HttpResponseRedirect, HttpResponse
from allauth.account.utils import complete_signup

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from .models import CustomUser
User = get_user_model()

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


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'custom_account/users.html'
    context_object_name = 'users'


    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            html = render_to_string(self.template_name, context, request=self.request)
            return HttpResponse(html)
        else:
            # Return a custom error page for non-HTMX requests
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html', {}, request=self.request)
            )

class UsersCreateView(CreateView):
    model = CustomUser
    template_name = 'custom_account/create.html'
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('custom_account:users-list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        group = form.cleaned_data.get('group')
        if group:
            user.groups.add(group)

        # Check if the request is an HTMX request
        if self.request.headers.get('HX-Request'):
            # If it's an HTMX request, render the updated user list
            html = render_to_string(
                'custom_account/create.html',
                {'users': CustomUser.objects.all()},
                request=self.request
            )
            return HttpResponse(html)

        # Else, return the custom error page for non-HTMX requests
        else:
            # Return forbidden response for non-HTMX requests
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html', {}, request=self.request)
            )

    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return HttpResponse(html, status=400)
        return super().form_invalid(form)