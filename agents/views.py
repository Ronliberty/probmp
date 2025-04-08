from lib2to3.fixes.fix_input import context
from msilib.schema import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView, DeleteView, UpdateView, ListView
from .models import AgentImage, OurAgent, Tickets, TicketStatus, Information
from .forms import  OurAgentForm, AgentImageForm, InformationForm, InformationImageForm, InformationVideoForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.db.models import Count

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

class TicketCreateView(CreateView):
    model = Tickets
    fields = ['subject', 'description', 'assigned_user', 'assigned_group']
    template_name = 'agents/tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TicketDetailView(DetailView):
    model = Tickets
    template_name = 'agents/tickets/ticket_detail.html'
    context_object_name = 'ticket'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class TicketUpdateView(UpdateView):
    model = Tickets
    fields = ['subject', 'description', 'assigned_user', 'assigned_group']
    template_name = 'agents/tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class TicketDeleteView(DeleteView):
    model = Tickets
    template_name = 'agents/tickets/confirm_delete.html'
    success_url = reverse_lazy('ticket-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class TicketListView(ListView):
    model = Tickets
    template_name = 'agents/tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_template_names(self):
        if not self.request.headers.get('HX-Request'):
            return ['custom_account/errors/htmx_only.html']

        user = self.request.user

        if user.is_superuser:
            return ['agents/tickets/ticket_super.html']
        elif user.groups.filter(name='manager').exists():
            return ['agents/tickets/ticket_manager.html']
        elif user.groups.filter(name='agent').exists():
            return ['agents/tickets/ticket-list.html']
        else:
            return ['agents/tickets/ticket_list.html']  # fallback for users with no group

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.groups.filter(name='agent').exists():
            return Tickets.objects.all().order_by('-created_at')
        return Tickets.objects.filter(owner=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_agent'] = self.request.user.groups.filter(name='agent').exists()
        context['is_manager'] = self.request.user.groups.filter(name='manager').exists()
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html', context, request=self.request)
            )
        return super().render_to_response(context, **response_kwargs)


class TicketEngageView(UserPassesTestMixin, UpdateView):
    model = Tickets
    fields = ['response']
    template_name = 'agents/tickets/ticket_engage_form.html'
    context_object_name = 'ticket'

    slug_url_kwarg = 'slug'

    def test_func(self):
        ticket = self.get_object()
        # Only superuser, manager, or assigned user can engage tickets
        if self.request.user.is_superuser:
            return True
        if self.request.user.groups.filter(name='manager').exists():
            return True
        if ticket.assigned_user == self.request.user or ticket.assigned_group in self.request.user.groups.all():
            return True
        return False

    def form_valid(self, form):
        # If a ticket is marked as RESOLVED or CLOSED, it can’t be changed anymore
        if form.instance.status in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
            return HttpResponseForbidden("You can't modify a resolved or closed ticket.")

        # Assign the user who responded
        form.instance.responded_by = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to ticket detail view after responding
        return reverse_lazy('ticket-detail', kwargs={'slug': self.object.slug})


class InformationCreateView(UserPassesTestMixin, CreateView):
    model = Information
    form_class = InformationForm
    template_name = 'agents/information/information_form.html'
    success_url = reverse_lazy('information-list')

    def test_func(self):
        # Only allow managers to create information
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        # Automatically set the owner (current user) before saving
        form.instance.owner = self.request.user
        information = form.save()

        # Handle Image Upload
        image_form = InformationImageForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            image_form.instance.information = information
            image_form.save()

        # Handle Video Upload
        video_form = InformationVideoForm(self.request.POST, self.request.FILES)
        if video_form.is_valid():
            video_form.instance.information = information
            video_form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = InformationImageForm()
        context['video_form'] = InformationVideoForm()
        return context




# Define the ListView for Information
class InformationListView(UserPassesTestMixin, ListView):
    model = Information
    template_name = 'agents/information/information_list.html'
    context_object_name = 'informations'


    def test_func(self):
        user =self.request.user
        return (
            user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__in=['manager', 'agent', 'default']).exists()
        )
        )

    def get_template_names(self):
        if not self.request.headers.get('HX-Request'):
            return ['custom_account/errors/htmx_only.html']

        user = self.request.user

        if user.is_superuser:
            return ['agents/information/infor_super.html']
        elif user.groups.filter(name='manager').exists():
            return ['agents/information/infor_manager.html']
        elif user.groups.filter(name='agent').exists():
            return ['agents/information/infor-list.html']
        else:
            return ['agents/information/information_list.html']



    def get_queryset(self):

        return Information.objects.all()
    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html', context, request=self.request)
            )
        return super().render_to_response(context, **response_kwargs)


# Define the DetailView for Information
class InformationDetailView(UserPassesTestMixin, DetailView):
    model = Information
    template_name = 'information/information_detail.html'
    context_object_name = 'information'

    def test_func(self):
        # Only allow managers to view the details of information
        return self.request.user.groups.filter(name='manager').exists()


# Define the DeleteView for Information
class InformationDeleteView(UserPassesTestMixin, DeleteView):
    model = Information
    template_name = 'information/confirm_delete.html'
    context_object_name = 'information'
    success_url = reverse_lazy('information-list')

    def test_func(self):
        # Only allow managers to delete information
        return self.request.user.groups.filter(name='manager').exists()

    def delete(self, request, *args, **kwargs):
        information = self.get_object()
        # Optionally, delete related images and videos
        information.images.all().delete()
        information.videos.all().delete()
        return super().delete(request, *args, **kwargs)

class TicketAnalysisView(TemplateView):
    template_name = 'agents/tickets/ticket_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Current date and time to use for filtering
        current_date = now()

        # Tickets data aggregated by day, month, and year for solved tickets
        tickets_per_day = Tickets.objects.filter(status='resolved').annotate(day=TruncDate('updated_at')).values('day').annotate(count=Count('id')).order_by('-day')
        tickets_per_month = Tickets.objects.filter(status='resolved').annotate(month=TruncMonth('updated_at')).values('month').annotate(count=Count('id')).order_by('-month')
        tickets_per_year = Tickets.objects.filter(status='resolved').annotate(year=TruncYear('updated_at')).values('year').annotate(count=Count('id')).order_by('-year')

        # Unsolved tickets by day, month, and year
        unsolved_tickets_per_day = Tickets.objects.filter(status='open').annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('-day')
        unsolved_tickets_per_month = Tickets.objects.filter(status='open').annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('-month')
        unsolved_tickets_per_year = Tickets.objects.filter(status='open').annotate(year=TruncYear('created_at')).values('year').annotate(count=Count('id')).order_by('-year')

        # Tickets that are still in progress
        in_progress_tickets = Tickets.objects.filter(status='in_progress').count()

        # Last solved ticket data (last 1 solved ticket)
        last_solved_ticket = Tickets.objects.filter(status='resolved').order_by('-updated_at').first()

        # Aggregate ticket statistics and pass them to the context
        context.update({
            'tickets_per_day': tickets_per_day,
            'tickets_per_month': tickets_per_month,
            'tickets_per_year': tickets_per_year,
            'unsolved_tickets_per_day': unsolved_tickets_per_day,
            'unsolved_tickets_per_month': unsolved_tickets_per_month,
            'unsolved_tickets_per_year': unsolved_tickets_per_year,
            'in_progress_tickets': in_progress_tickets,
            'last_solved_ticket': last_solved_ticket,
            'current_date': current_date,
        })

        return context
    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html', context, request=self.request)
            )
        return super().render_to_response(context, **response_kwargs)

