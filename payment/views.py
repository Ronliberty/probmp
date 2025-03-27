

from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, ListView
from .models import Analytics, Invoice
from django.urls import reverse_lazy
from .forms import AnalyticForm, InvoiceForm



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
    template_name = 'payment/list.html'
    context_object_name = 'invoices'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





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