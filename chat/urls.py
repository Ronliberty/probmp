from django.urls import path
from .views import ChartView, ChatRoomCreateView, ChatRoomListView
from . import views
app_name = 'chat'

urlpatterns = [
    path('chat/', ChartView.as_view(), name='chart' ),
    path('rooms/', views.load_rooms, name='load_rooms'),
    path("messages/<int:group_id>/", views.load_messages, name="load_messages"),
    path('create-room/', ChatRoomCreateView.as_view(), name='create_room'),
    path('rooms/', ChatRoomListView.as_view(), name='room_list'),

]