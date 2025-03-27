from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.shortcuts import render, get_object_or_404
from .models import ChatGroup, GroupMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ChatGroupForm
# Create your views here.
class ChartView(TemplateView):
    template_name = 'chat/chat.html'


def load_rooms(request):
    chat_groups = ChatGroup.objects.all()
    return render(request, "chat/partials/room_list.html", {"chat_groups": chat_groups})


def load_messages(request, group_id):
    """Fetches messages for a specific chat room."""
    chat_group = get_object_or_404(ChatGroup, id=group_id)
    messages = GroupMessage.objects.filter(group=chat_group).order_by("timestamp")

    return render(request, "chat/partials/message_list.html", {"messages": messages})

class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = ChatGroup
    form_class = ChatGroupForm
    template_name = 'chat/chat_create_room.html'
    success_url = reverse_lazy('chat:room_list')  # Redirect after creation

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set creator
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)  # Add creator as first member
        return response


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatGroup
    template_name = 'chat/chat_room_list.html'
    context_object_name = 'rooms'