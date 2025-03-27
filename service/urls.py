from django.urls import path
from .views import ServiceView, RequestView, CreateServiceView, ServiceListView, DeleteServiceView, DetailServiceView, UserDetailServiceView, CreateRequestServiceView, CreateResponseView, DetailRequestView, DetailUserRequestView, DeleteUserRequestView, RequestListsView, DetailResponseView, ListResponseView, UserResponseView, UserDetailedResponseView, DeleteResponseView

app_name = 'service'

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service-list'),



    #Manger

    path('create/service/', CreateServiceView.as_view(), name='service-create'),
    path('service/list/', ServiceListView.as_view(), name='service-manager'),
    path('delete/service/<slug:slug>/', DeleteServiceView.as_view(), name='delete-service'),
    path('manager/detail/<slug:slug>/', DetailServiceView.as_view(), name='detail-manager'),
    path('detail/service/<slug:slug>/', UserDetailServiceView.as_view(), name='detail-user' ),



    #requets
    #default
    path('create/request/', CreateRequestServiceView.as_view(), name='request-create'),
    path('request', RequestView.as_view(), name='request-list'),
    path('user/request/<slug:slug>/', DetailUserRequestView.as_view(), name='user-request'),
    path('delete/request/<slug:slug>/', DeleteUserRequestView.as_view(), name='delete-request'),

    #manager
    path('detail/request/<slug:slug>/', DetailRequestView.as_view(), name='detail-request'),
    path('list/requests/', RequestListsView.as_view(), name='list-manager'),


    #response
    #manager
    path('create/response/<slug:slug>/', CreateResponseView.as_view(), name='response-create'),
    path('response/detail/<slug:slug>/', DetailResponseView.as_view(), name='detail-response'),
    path('list/response/', ListResponseView.as_view(), name='list-response'),
    path('delete/response/<slug:slug>/', DeleteResponseView.as_view(), name='delete-response'),

    #default
    path('user/response/', UserResponseView.as_view(), name='user-response'),
    path('detailed/response/<slug:slug>/', UserDetailedResponseView.as_view(), name='detailed-response'),

]