from django.urls import path


from .views import PartnerView, PartnerCreateView, ManagerRequestListView,  PartnerUserDetailView, PartnerManagerDetailView, PartnerListView, PartnerDeleteView, PartnershipRequestView, UserRequestView, PartnershipUserDetailView, DeletePartnershipView, RequestResponseView, ResponseListView, DeleteResponseView


app_name = 'partner'

urlpatterns = [
    #default
    path('partner', PartnerView.as_view(), name='partner-list'),
    path('partner/detail/<slug:slug>/', PartnerUserDetailView.as_view(), name='user-detail'),

    #manager
    path('partner/create/', PartnerCreateView.as_view(), name='partnership-create'),

    path('partner/detail/<slug:slug>/', PartnerManagerDetailView.as_view(), name='manager-detail'),
    path('partner/list/', PartnerListView.as_view(), name='partnership-list'),

    path('partner/delete/<slug:slug>/', PartnerDeleteView.as_view(), name='partnership-delete'),

    # requests
    #default
    path('partnership/request/', PartnershipRequestView.as_view(), name='partner-request'),

    path('list/partnership/', UserRequestView.as_view(), name='user-request'),

    path('detailed/request/', PartnershipUserDetailView.as_view(), name='detailed-request'),

    path('delete/partnership/', DeletePartnershipView.as_view(), name='delete-partnership'),

    #manager

    path('respond/request/', RequestResponseView.as_view(), name='response-request'),
    path('manager/requests/', ManagerRequestListView.as_view(), name='request-manager'),

    path('response/list/', ResponseListView.as_view(), name='response-list'),

    path('response/delete/', DeleteResponseView.as_view(), name='delete-response'),

]