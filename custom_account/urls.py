from django.urls import path
from .views import SettingsView, AccountView, ProfileView, HelpView, PoliciesView, NotificationsView, RedirectAfterLoginView, CustomUserSignupView, CustomUserLoginView
from django.contrib.auth.views import LogoutView

app_name = 'custom_account'

urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings-menu'),
    path('custom_account/', AccountView.as_view(), name='custom_account-settings'),
    path('profile/', ProfileView.as_view(), name='profile-settings'),
    path('help/', HelpView.as_view(), name='help-settings'),
    path('policies/', PoliciesView.as_view(), name='policy-settings'),
    path('notify/', NotificationsView.as_view(), name='notify-settings'),
    path('redirect/', RedirectAfterLoginView.as_view(), name='redirect_after_login'),
    path("signup/", CustomUserSignupView.as_view(), name="account_signup"),
    path("login/", CustomUserLoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(next_page="account_login"), name="account_logout"),

]

