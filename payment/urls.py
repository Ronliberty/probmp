from django.urls import path
from .views import AnalyticsView, InvoiceView, InvoiceListView, UserInvoiceDetailView, InvoiceDetailView, CreateInvoiceView, InvoiceDeleteView, CreateAnalyticView, AnalyticsDetailView, UserAnalyticDetailView, AnalyticsDeleteView, AnalyticsListView


app_name = 'payment'

urlpatterns = [

    #invoice

    path('invoice', InvoiceView.as_view(), name='invoice-list'),
    path('list/invoice/', InvoiceListView.as_view(), name='invoice-manager'),
    path('create/invoice', CreateInvoiceView.as_view(), name='create-invoice'),
    path('detail/invoice/', InvoiceDetailView.as_view(), name='manager-invoice'),
    path('invoice/detail/', UserInvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),



    #analytics
    path('analytics/', AnalyticsView.as_view(), name='analytics-list'),
    path('list/analytics/', AnalyticsListView.as_view(), name='manager-list'),
    path('create/analytics/', CreateAnalyticView.as_view(), name='create-analytic'),
    path('detail/analytic/', AnalyticsDetailView.as_view(), name='manager-detail'),
    path('detail/', UserAnalyticDetailView.as_view(), name='user-detail'),
    path('delete/', AnalyticsDeleteView.as_view(), name='analytic-delete'),




]