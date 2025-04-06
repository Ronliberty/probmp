from lib2to3.fixes.fix_input import context
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from payment.models import Invoice
from decimal import Decimal
User = get_user_model()

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
    group_name = None
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.group_name and not request.user.groups.filter(name=self.group_name).exists():
            messages.error(request, "You are not authorized to access this page")
            return redirect('base:index')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get recent users
        context['users'] = User.objects.all().order_by('-last_login')[:10]

        # Financial metrics from paid invoices
        paid_invoices = Invoice.objects.filter(status='paid', is_deleted=False)

        # Total revenue (sum of all paid invoices)
        total_revenue = paid_invoices.aggregate(total=Sum('amount_to_pay'))['total'] or 0
        context['total_revenue'] = total_revenue

        # For demo purposes, let's assume expenses are 50% of revenue
        # In a real app, you would calculate this from your Expense model
        total_expenses = total_revenue * Decimal('0.5')
        context['total_expenses'] = total_expenses

        # Net profit
        context['net_profit'] = total_revenue - total_expenses

        # Monthly profit data for chart
        months = []
        monthly_profit = []

        for i in range(5, -1, -1):  # Last 6 months
            month_start = timezone.now().replace(
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ) - timedelta(days=30 * i)

            month_end = month_start + timedelta(days=30)

            month_revenue = Invoice.objects.filter(
                status='paid',
                created_at__gte=month_start,
                created_at__lt=month_end
            ).aggregate(total=Sum('amount_to_pay'))['total'] or 0

            month_expense = month_revenue * Decimal('0.5')  # Again, replace with real expense calculation
            month_profit = month_revenue - month_expense

            months.append(month_start.strftime('%b %Y'))
            monthly_profit.append(float(month_profit))

        context['months'] = months
        context['monthly_profit'] = monthly_profit

        # Revenue vs Expenses data for chart
        context['revenue_vs_expenses'] = {
            'revenue': float(total_revenue),
            'expenses': float(total_expenses)
        }

        return context


class AgentDashboardView(BaseDashboardView):
    template_name = 'dashboard/agent_dash.html'
    group_name = 'agent'

class ManagerDashboard(BaseDashboardView):
    template_name = 'dashboard/manger_dash.html'
    group_name = 'manager'