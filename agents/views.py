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
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponse
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
    template_name = "agents/agent_form.html"  # Default template

    def get_template_names(self):
        if self.request.user.is_superuser:
            return ["agents/create_agent.html"]
        return [self.template_name]

    def post(self, request, *args, **kwargs):
        # Early return for non-HTMX requests
        if not request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html', {}, request=self.request)
            )

        form = OurAgentForm(request.POST)
        image_form = AgentImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            agent = form.save()
            for image in request.FILES.getlist('images'):
                AgentImage.objects.create(agent=agent, image=image)

            messages.success(request, "Agent created successfully!")

            return JsonResponse({
                'message': 'Agent created successfully!',
                'html': render_to_string('agents/agent_detail.html', {'agent': agent})
            })

        # Handle invalid form case
        return JsonResponse({
            'message': 'There was an error creating the agent.',
            'html': render_to_string('agents/errors.html', {
                'form': form,
                'image_form': image_form
            })
        }, status=400)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            template_name = self.get_template_names()[0]
            html = render_to_string(template_name, context, request=self.request)
            return HttpResponse(html)
        return HttpResponseForbidden(
            render_to_string('custom_account/errors/htmx_only.html', {}, request=self.request)
        )

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


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