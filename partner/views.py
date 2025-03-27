from msilib.schema import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Partnership, PartnershipRequest, AcceptedPartnership
from .forms import PartnershipForm, RequestForm, ResponseForm
from django.http import JsonResponse
from django.template.loader import render_to_string



class PartnerView(LoginRequiredMixin, ListView):
    model = Partnership
    template_name = 'partner/partner_list.html'
    context_object_name = 'partnerships'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, self.get_context_data())
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)





class PartnerCreateView(LoginRequiredMixin, CreateView):
    model = Partnership
    template_name = 'partner/create.html'
    form_class = PartnershipForm
    success_url = reverse_lazy('partner:partnership-list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)





class PartnerUserDetailView(LoginRequiredMixin, DetailView):
    model = Partnership
    template_name = 'partner/user-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'partnerships'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()


class PartnerManagerDetailView(TemplateView):
    model = Partnership
    template_name = 'partner/manager-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'partnerships'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class PartnerListView(TemplateView):
    model = Partnership
    template_name = 'partner/list.html'
    context_object_name = 'partnerships'



    def get_queryaset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Partnership.objects.all()
        return Partnership.objects.none()




class PartnerDeleteView(LoginRequiredMixin, DeleteView):
    model = Partnership
    template_name = 'partner/delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('partner:partnership-list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



#request


class PartnershipRequestView(CreateView):
    model = PartnershipRequest
    form_class = RequestForm
    template_name = 'partner/request-list.html'
    success_url = reverse_lazy('partner:user-request')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UserRequestView(ListView):
    model = PartnershipRequest
    template_name = 'partner/user-request.html'
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()




class PartnershipUserDetailView(DetailView):
    model = PartnershipRequest
    template_name = 'partner/user-detailed.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()




class DeletePartnershipView(DeleteView):
    model = PartnershipRequest
    template_name = 'partner/delete-partnership.html'
    success_url = reverse_lazy('partner:user-request')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()



class ManagerRequestListView(ListView):
    model = PartnershipRequest
    template_name = 'partner/manager-request.html'
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

class RequestResponseView(CreateView):
    model = AcceptedPartnership
    form_class = ResponseForm
    template_name = 'partner/request.html'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class ResponseListView(ListView):
    model = AcceptedPartnership
    template_name = 'partner/response-list.html'
    context_object_name = 'accepted'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





class DeleteResponseView(DeleteView):
    model = AcceptedPartnership
    template_name = 'partner/response-delete.html'
    success_url = reverse_lazy('partner:user-request')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




