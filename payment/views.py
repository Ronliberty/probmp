from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, ListView
from .models import Analytics, Invoice
from django.urls import reverse_lazy
from .forms import AnalyticForm, InvoiceForm
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden


class FinancialDashboardView(TemplateView):
    template_name = 'payment/financials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here
        context['page_title'] = 'Financial Dashboard'
        return context
    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html',
                                 context,
                                 request=self.request)
            )
        return super().render_to_response(context, **response_kwargs)

class AnalyticsView(ListView):
    model = Analytics
    template_name = 'payment/anaylitcs.html'
    context_object_name = 'analytics'





class InvoiceView(ListView):
    model = Invoice
    template_name = 'payment/invoice.html'
    context_object_name = 'invoices'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()




class InvoiceListView(ListView):
    model = Invoice

    context_object_name = 'invoices'

    def get_template_names(self):
        if not self.request.headers.get('HX-Request'):
            return ['custom_account/errors/htmx_only.html']

        if self.request.user.is_superuser:
            return ['payment/list_payment.html']  # Special template for superusers
        return ['payment/list.html']  # Regular template for managers

    def get_queryset(self):
        # Allow access to both managers and superusers
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset()

        # Add user type to context if needed for template differences
        context['is_superuser'] = self.request.user.is_superuser
        context['is_manager'] = self.request.user.groups.filter(name='manager').exists()

        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html',
                                 context,
                                 request=self.request)
            )
        return super().render_to_response(context, **response_kwargs)


class UserInvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'payment/user-invoice.html'
    context_object_name = 'invoices'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()




class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'payment/detail-invoice.html'
    context_object_name = 'invoices'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





class CreateInvoiceView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'payment/create-invoice.html'
    success_url = reverse_lazy('payment:invoice-manager')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = 'payment/delete-invoice.html'
    success_url = reverse_lazy('payment:invoice-manager')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





class CreateAnalyticView(CreateView):
    model = Analytics
    form_class = AnalyticForm
    template_name = 'payment/create-analytics.html'
    success_url = reverse_lazy('payment:manager-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)







class AnalyticsDetailView(DetailView):
    model = Analytics
    template_name = 'payment/detail-analytics.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'analytics'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()






class UserAnalyticDetailView(TemplateView):
    model = Analytics
    template_name = 'payment/user-analytics.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'analytics'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()





class AnalyticsDeleteView(DeleteView):
    model = Analytics
    template_name = 'payment/delete-analytics.html'
    success_url = reverse_lazy('payment:manager-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





class AnalyticsListView(ListView):
    model = Analytics
    template_name = 'payment/list-analytics.html'
    context_object_name = 'analytics'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()