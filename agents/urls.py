from django.urls import path
from .views import AgentView, AgentCreateView, AgentListView, AgentDeleteView, AgentDetailView, AgentUserDetailView, AgentUpdateView


app_name = 'agents'

urlpatterns = [
    #default
    path('detail/agent/<slug:slug>/', AgentUserDetailView.as_view(), name='agent-detagent-det'),
    path('agents/', AgentView.as_view(), name='agents-list'),

    #manager


    path('create/agent/', AgentCreateView.as_view(), name='agent-create'),
    path('list/agent/', AgentListView.as_view(), name='agents-manager'),
    path('detail/agent/<slug:slug>/', AgentDetailView.as_view(), name='agent-detail'),
    path('delete/agent/<slug:slug>/', AgentDeleteView.as_view(), name='agent-delete'),
    path("agents/<slug:slug>/update/", AgentUpdateView.as_view(), name="agent-update"),
]