
from django.urls import path
from .views import UserDashboardView, HistoryView, AgentDashboardView, ManagerDashboard, SuperDashboard

app_name = 'dashboard'
urlpatterns = [
    path('user_dashboard/', UserDashboardView.as_view(), name='user_dashboard' ),
    path('agent/', AgentDashboardView.as_view(), name='agent-dashboard'),
    path('manager/', ManagerDashboard.as_view(), name='manager-dashboard'),
    path('super/', SuperDashboard.as_view(), name='super-dash'),
    path('history/', HistoryView.as_view(), name='history'),
]