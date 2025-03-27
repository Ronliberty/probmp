from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DeleteView, DetailView, ListView
from urllib3 import request
from django.urls import reverse_lazy
from .models import Service, ServiceRequest, ServiceResponse
from .forms import ServiceForm, RequestServiceForm, ResponseForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from custom_account.models import Notification
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import timedelta

class ServiceView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service/service-list.html'
    context_object_name = 'services'

    def get_queryset(self):
        user = self.request.user
        queryset = Service.objects.all()

        # Search Filter
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Country Filter
        country_filter = self.request.GET.get('country')
        if country_filter:
            queryset = queryset.filter(country__iexact=country_filter)

        # If the user is in 'default' group, show all services
        if user.groups.filter(name='default').exists():
            return queryset

        # Get user-requested services
        user_services = ServiceRequest.objects.filter(requested_by=user).values_list('service_id', flat=True)

        # Get trending services in the last 30 days
        last_30_days = now() - timedelta(days=30)
        trending_services = Service.objects.annotate(
            request_count=Count('requests', filter=Q(requests__requested_at__gte=last_30_days))
        ).order_by('-request_count')[:5]

        # Show user-requested and trending services
        queryset = queryset.filter(Q(id__in=user_services) | Q(id__in=[s.id for s in trending_services]))

        return queryset.distinct()







class CreateServiceView(LoginRequiredMixin, CreateView):
    model = Service
    template_name = 'service/create-service.html'
    context_object_name = 'services'
    form_class = ServiceForm
    success_url = reverse_lazy ('service:service-manager')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service/list-service.html'
    context_object_name = 'services'



    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Service.objects.all()
        return Service.objects.none()



class DeleteServiceView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service/delete-service.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = 'service:service-manager'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class DetailServiceView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'service/manager-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'services'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class UserDetailServiceView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'service/user-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()




#response class
class DetailRequestView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'service/manager-request.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'request'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




class DetailUserRequestView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'service/user-request.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'requests'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()




class DeleteUserRequestView(LoginRequiredMixin, DeleteView):
    model = ServiceRequest
    template_name = 'service/request-delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = 'service:request-list'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()





class RequestListsView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'service/request-manager.html'
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()






class CreateRequestServiceView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = RequestServiceForm
    template_name = 'service/create-request.html'
    success_url = reverse_lazy ('service:request-list')

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()
    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        if not form.instance.service:
            form.add_error('service', 'Service is required.')
            return self.form_invalid(form)
        return super().form_valid(form)




class RequestView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'service/request-service.html'
    context_object_name = 'requests'

    def get_queryset(self):
        if self.request.user.groups.filter(name='default').exists():
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.none()



class DetailResponseView(LoginRequiredMixin, DetailView):
    model = ServiceResponse
    template_name = 'service/response-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'response'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





class UserResponseView(LoginRequiredMixin, ListView):
    model = ServiceResponse
    template_name = 'service/list-response.html'
    context_object_name = 'response'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, self.get_context_data())
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)


class CreateResponseView(LoginRequiredMixin, CreateView):
    model = ServiceResponse
    template_name = 'service/response_create.html'
    context_object_name = 'response'
    form_class = ResponseForm
    success_url = reverse_lazy('service:list-response')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


    def form_valid(self, form):
        form.instance.responded_by = self.request.user
        response = form.save()

        # ✅ Create a notification
        self.create_notification(response.service_request)
        return super().form_valid(form)

    def create_notification(self, service_request):
        """
        Function to create a notification when a service request is approved.
        """
        Notification.objects.create(
            user=service_request.requested_by,  # Send notification to the requester
            message=f"Your service request '{service_request.service.name}' has been approved."
        )




class ListResponseView(LoginRequiredMixin, ListView):
    model = ServiceResponse
    template_name = 'service/manager-response-list.html'
    context_object_name = 'response'

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.none()


class UserDetailedResponseView(LoginRequiredMixin, DetailView):
    model = ServiceResponse
    template_name = 'service/response-user.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()






class DeleteResponseView(LoginRequiredMixin, DeleteView):
    model = ServiceResponse
    template_name = 'service/delete-response.html'
    context_object_name = 'response'
    success_url = 'service:list-response'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()











