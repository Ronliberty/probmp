from msilib.schema import ListView
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from allauth.account.models import Login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Post, News, Tool, Skill
from .forms import PostForm, NewsForm, ToolForm, SkillForm
# Create your views here.


class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'freelance/post.html'
    context_object_name = 'post'



    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an AJAX request
            html = render_to_string(self.template_name, self.get_context_data())
            return JsonResponse({'html': html})  # Return JSON containing the HTML
        return super().get(request, *args, **kwargs)





class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'freelance/post-user.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = 'Post'
    form_class = PostForm
    template_name = 'freelance/create_post.html'
    success_url = reverse_lazy('freelance:list-post')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



class PostManagerDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'freelance/post-manager.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'freelance/post-list.html'
    context_object_name = 'posts'


    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Post.objects.all()
        return Post.objects.none()

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Ensure it's an AJAX request
            posts = self.get_queryset()
            data = [
                {
                    "id": post.id,
                    "title": post.title,
                    "country": post.country if post.country else "N/A",
                    "status": post.status,
                    "created_by": post.created_by.username,
                    "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
                    "slug": post.slug
                }
                for post in posts
            ]
            return JsonResponse({"posts": data}, status=200)

        return super().get(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'freelance/post-delete.html'
    success_url = reverse_lazy('freelance:list-post')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()





class NewsView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'freelance/partials/news_list.html'
    context_object_name = 'news_list'
    # Partial template for HTMX

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

    def render_to_response(self, context, **response_kwargs):
        """Only return partial if request is from HTMX"""
        if self.request.headers.get('HX-Request'):
            return render(self.request, self.template_name, context)
        return HttpResponse("Invalid request", status=400)

class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'freelance/news-user.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'news_list'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()





#management
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'freelance/news-create.html'
    form_class = NewsForm
    success_url = reverse_lazy('freelance:list-news')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class NewsManagerDetailView(LoginRequiredMixin, UserPassesTestMixin,  DetailView):
    model = News
    template_name = 'freelance/news-manager.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'news_list'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def get_queryset(self):
        return News.objects.all()


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'freelance/news-list.html'
    context_object_name = 'news_list'


    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return News.objects.all()
        return News.objects.none()

    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string('custom_account/errors/htmx_only.html',
                                 context,
                                 request=self.request)
            )
        return super().render_to_response(context, **response_kwargs)


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'freelance/news-delete.html'
    success_url = reverse_lazy('freelance:list-news')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class ToolsView(LoginRequiredMixin, ListView):
    model = Tool
    template_name = 'freelance/tools.html'
    context_object_name = 'tools'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, self.get_context_data())
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)




class ToolsDetailView(LoginRequiredMixin, DetailView):
    model = Tool
    template_name = 'freelance/user-tools.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'tools'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()



class ToolsCreateView(LoginRequiredMixin, CreateView):
    model = Tool
    form_class = ToolForm
    template_name = 'freelance/tools-create.html'
    success_url = reverse_lazy('freelance:list-tools')



    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



class ToolsManagerDetailView(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = Tool
    template_name = 'freelance/tools-manager.html'
    context_object_name = 'tools'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'



    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def get_queryset(self):
        return Tool.objects.all()




class ToolsListView(LoginRequiredMixin, ListView):
    model = Tool
    template_name = 'freelance/tools-list.html'
    context_object_name = 'tools'

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Tool.objects.all()
        return Tool.objects.none()


    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class ToolsDeleteView(LoginRequiredMixin, DeleteView):
    model = Tool
    template_name = 'freelance/delete-tools.html'
    success_url = reverse_lazy('freelance:list-tools')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




class SkillsView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = 'freelance/skills.html'
    context_object_name = 'skills'

    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, self.get_context_data())
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)



class SkillsDetailView(LoginRequiredMixin, DetailView):
    model = Skill
    template_name = 'freelance/user-skill.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'skills'
    def test_func(self):
        return self.request.user.groups.filter(name='default').exists()


class SkillsCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'freelance/create-skill.html'
    success_url = reverse_lazy('freelance:list-skills')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class SkillsManagerDetailView(LoginRequiredMixin, DetailView):
    model = Skill
    template_name = 'freelance/skill-manager.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'skills'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




class SkillsListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Skill
    template_name = 'freelance/skill-list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Skill.objects.all()
        return Skill.objects.none()

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




class SkillsDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = 'freelance/skill-delete.html'
    success_url = reverse_lazy('freelance:list-skills')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()






