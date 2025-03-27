from django.shortcuts import render ,redirect,  get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import HeroContent, Step, Service, Testimonial, ContactSubmission, SocialLink
from django.contrib import messages
from .forms import HeroContentForm, ContactForm, ServiceForm, SocialLinkForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse
from django.urls import reverse


def is_manager(user):
    return user.groups.filter(name='managers').exists()


class IndexView(TemplateView):
    template_name = 'base/index.html'

@method_decorator(cache_page(60 * 15), name='dispatch')
class InfoContentView(TemplateView):
    template_name = 'base/info.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the form to the context for GET requests
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save the valid form data to ContactSubmission
            # (assuming your form's save() method handles this)
            form.save()
            messages.success(request, "Your message has been submitted successfully!")
            return redirect('base:index')  # Redirect to prevent form resubmission
        else:
            # Re-render the template with form errors
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(
                self.get_context_data(form=form)
            )





class ErrorView(TemplateView):
    template_name = 'base/error.html'

class ContactSubmissionListView(ListView):
    model = ContactSubmission
    template_name = 'base/contact/list.html'
    context_object_name = 'submissions'

    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

class ContactSubmissionDetailView(DetailView):
    model = ContactSubmission
    template_name = 'base/contact/detail.html'
    context_object_name = 'submission'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class SocialLinkCreateView(CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = 'base/socials/create.html'
    success_url = reverse_lazy('base:sociallink-list')

    def form_valid(self, form):
        # Automatically set slug from platform before saving
        instance = form.save(commit=False)
        instance.save()  # This triggers the slug generation
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class SocialLinkListView(ListView):
    model = SocialLink
    template_name = 'base/socials/list.html'
    context_object_name = 'social_links'
    paginate_by = 10

    def get_queryset(self):
        return SocialLink.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

class SocialLinkDetailView(DetailView):
    model = SocialLink
    template_name = 'base/socials/detail.html'
    context_object_name = 'social_link'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

class SocialLinkDeleteView(DeleteView):
    model = SocialLink
    template_name = 'base/socials/delete.html'
    success_url = reverse_lazy('base:sociallink-list')
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class HeroSectionView(View):
    def get(self, request, *args, **kwargs):
        hero_content = HeroContent.objects.filter(is_active=True).first()
        return render(request, "base/partials/hero_section.html", {"hero_content": hero_content})




class HeroContentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = HeroContent
    form_class = HeroContentForm
    template_name = 'base/hero/hero_content_form.html'
    success_url = reverse_lazy('base:hero_content_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

class HeroContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HeroContent
    form_class = HeroContentForm
    template_name = 'base/hero/hero_content_form.html'
    success_url = reverse_lazy('base:hero_content_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class HeroListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = HeroContent
    template_name = 'base/hero/hero_list.html'
    context_object_name = 'object_list'  # Use this in the template

    required_role = 'manager'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def get_queryset(self):
        return HeroContent.objects.all()  # Fix: Use `.all()` instead of `.all`

    def render_to_response(self, context, **response_kwargs):
        """Return the correct template if HTMX is used, else return 400"""
        if self.request.headers.get('HX-Request'):
            return render(self.request, self.template_name, context)
        return HttpResponse("Invalid request", status=400)
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)





class HeroDeleteView(UserPassesTestMixin, DeleteView):
    model = HeroContent
    template_name = 'base/hero/hero_confirm_delete.html'
    success_url = reverse_lazy('base:hero_content_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class HowItWorksView(View):
    def get(self, request, *args, **kwargs):
        steps = Step.objects.all()
        return render(request, "base/partials/how_it_works.html", {"steps": steps})



class StepListView(ListView):
    model = Step
    template_name = "base/step/step_list.html"
    context_object_name = "steps"
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

class StepDetailView(DetailView):
    model = Step
    template_name = "base/step/step_detail.html"
    context_object_name = "step"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class StepCreateView(CreateView):
    model = Step
    template_name = "base/step/step_form.html"
    fields = ["title", "description", "step_number", "delay"]  # Excluding slug since it auto-generates
    success_url = reverse_lazy("base:step-list")

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)  # Ensure slug is set
        return super().form_valid(form)
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class StepUpdateView(UpdateView):
    model = Step
    template_name = "base/step/step_form.html"
    fields = ["title", "description", "step_number", "delay"]
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("base:step-list")
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)



class StepDeleteView(DeleteView):
    model = Step
    template_name = "base/step/step_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("base:step-list")
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class ServiceSectionView(View):
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        return render(request, "base/partials/service_list.html", {"services": services})




class ServiceListView(View):
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        return render(request, "base/service/service_list.html", {"services": services})
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

# Create View
class ServiceCreateView(CreateView):
    model = Service
    template_name = "base/service/service_form.html"
    fields = ["title", "description", "icon_url", "features"]
    success_url = reverse_lazy("base:service-list")

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)  # Ensure slug is set before saving
        return super().form_valid(form)
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

# Update View
class ServiceUpdateView(View):
    def get(self, request, slug, *args, **kwargs):
        service = get_object_or_404(Service, slug=slug)
        form = ServiceForm(instance=service)
        return render(request, "base/service/service_form.html", {"form": form, "service": service})
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        service = get_object_or_404(Service, slug=slug)
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect(reverse("base:service-list"))
        return render(request, "base/service_form.html", {"form": form, "service": service})
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

# Delete View
class ServiceDeleteView(View):
    def post(self, request, slug, *args, **kwargs):
        service = get_object_or_404(Service, slug=slug)
        service.delete()
        return JsonResponse({"message": "Service deleted successfully"}, status=200)
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)




class TestimonialSectionView(View):
    def get(self, request, *args, **kwargs):
        testimonials = Testimonial.objects.all().order_by('-id')[:3]
        return render(request, "base/partials/testimonial_section.html", {"testimonials": testimonials})



class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'base/testimonial/list.html'
    context_object_name = 'testimonials'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return 'base/testimonial/list.html'
        return super().get_template_names()
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class TestimonialCreateView(CreateView):
    model = Testimonial
    template_name = 'base/testimonial/form.html'
    fields = ['name', 'role', 'image_url', 'content', 'rating']
    success_url = reverse_lazy('base:testimonial-list')
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'base/testimonial/list.html',
                          {'testimonials': Testimonial.objects.all()})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'base/testimonial/form.html', {'form': form})
        return super().form_invalid(form)


class TestimonialUpdateView(UpdateView):
    model = Testimonial
    template_name = 'base/testimonial/form.html'
    fields = ['name', 'role', 'image_url', 'content', 'rating']
    success_url = reverse_lazy('base:testimonial-list')
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'base/testimonial/list.html',
                          {'testimonials': Testimonial.objects.all()})
        return response


class TestimonialDeleteView(DeleteView):
    model = Testimonial
    success_url = reverse_lazy('base:testimonial-list')

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return 'base/testimonial/confirm_delete.html'
        return 'base/testimonial/confirm_delete.html'
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)


class TestimonialDetailView(DetailView):
    model = Testimonial
    template_name = 'base/testimonial/detail.html'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return 'base/testimonial/detail.html'
        return super().get_template_names()
    def get(self, request, *args, **kwargs):
        is_htmx = self.request.headers.get('HX-Request') == 'true'

        if not is_htmx:
            self.template_name = 'dashboard/manager_dashboard.html' # Redirect non-HTMX requests

        return super().get(request, *args, **kwargs)























