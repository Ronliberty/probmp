from lib2to3.fixes.fix_input import context
from msilib.schema import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView, DeleteView, UpdateView, ListView
from .models import AgentImage, OurAgent
from .forms import  OurAgentForm, AgentImageForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
class AgentView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = OurAgent
    template_name = 'agents/list.html'
    context_object_name = 'agents'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

class AgentUserDetailView(LoginRequiredMixin, DetailView):
    model = OurAgent
    template_name = 'agents/detail.html'
    context_object_name = 'agent'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

class AgentDetailView(LoginRequiredMixin, DetailView):
    model = OurAgent
    template_name = 'agents/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class AgentCreateView(CreateView):
    model = OurAgent
    form_class = OurAgentForm
    template_name = "agents/agent_form.html"
    success_url = reverse_lazy("agents:agents-manager")

    def post(self, request, *args, **kwargs):
        form = OurAgentForm(request.POST)
        image_form = AgentImageForm(request.POST, request.FILES)

        if form.is_valid():
            agent = form.save()
            images = request.FILES.getlist('images')  # Get multiple files

            for image in images:
                AgentImage.objects.create(expert=agent, image=image)

            messages.success(request, "Agent created successfully!")
            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form, image_form=image_form))
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class AgentUpdateView(UpdateView):
    model = OurAgent
    form_class = OurAgentForm
    template_name = "agents/agent_form.html"
    success_url = reverse_lazy("agents:agents-manager")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = AgentImageForm(request.POST, request.FILES)

        if form.is_valid():
            self.object = form.save()
            images = request.FILES.getlist('images')

            for image in images:
                AgentImage.objects.create(agent=self.object, image=image)

            messages.success(request, "Agent updated successfully!")
            return redirect(self.success_url)

        def test_func(self):
            return self.request.user.groups.filter(name='manager').exists()

        return self.render_to_response(self.get_context_data(form=form, image_form=image_form))
class AgentListView(LoginRequiredMixin, ListView):
    model = OurAgent
    template_name = 'agents/manager-list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return OurAgent.objects.all()


class AgentDeleteView(LoginRequiredMixin, DeleteView):
    model = OurAgent, AgentImage
    template_name = 'agent/delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('agents:agents-manager')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()