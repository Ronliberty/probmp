from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseDashboardView(LoginRequiredMixin, TemplateView):
    group_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=self.group_name).exists():
            messages.error(request, "You are not authorized to access this page.")
            return redirect('base:index')
        return super().dispatch(request, *args, **kwargs)



class UserDashboardView(BaseDashboardView):
    template_name = 'dashboard/user_dashboard.html'
    group_name = 'default'

class HistoryView(TemplateView):
    template_name = 'dashboard/history.html'


class SuperDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/super_dash.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.group_name and not request.user.groups.filter(name=self.group_name).exists():
            messages.error(request, "You are not authorized to access this page")
            return redirect('base:index')

        return super().dispatch(request, *args, **kwargs)


class AgentDashboardView(BaseDashboardView):
    template_name = 'dashboard/agent_dash.html'
    group_name = 'agent'

class ManagerDashboard(BaseDashboardView):
    template_name = 'dashboard/manger_dash.html'
    group_name = 'manager'