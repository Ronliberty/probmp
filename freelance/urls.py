from django.urls import path
from .views import PostView,PostCreateView,  PostDetailView, PostManagerDetailView, PostListView, PostDeleteView, SkillsView, SkillsDetailView, SkillsCreateView, SkillsManagerDetailView, SkillsListView, SkillsDeleteView, ToolsView, ToolsDetailView, ToolsCreateView, ToolsManagerDetailView, ToolsListView, ToolsDeleteView, NewsView, NewsCreateView,  NewsDetailView, NewsManagerDetailView, NewsListView, NewsDeleteView

app_name = 'freelance'

urlpatterns = [
    #post
    path('post/', PostView.as_view(), name='post-list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),

    #manager
    path('create/post/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/', PostManagerDetailView.as_view(), name='post-det'),

    path('list/post/', PostListView.as_view(), name='list-post'),
    path('delete/post/<slug:slug>/', PostDeleteView.as_view(), name='delete-post'),




    #news
    path('news/', NewsView.as_view(), name='news-list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),

    # manager
    path('create/news/', NewsCreateView.as_view(), name='news-create'),
    path('news/<slug:slug>/', NewsManagerDetailView.as_view(), name='news-det'),
    path('list/news/', NewsListView.as_view(), name='list-news'),
    path('delete/news/<slug:slug>/', NewsDeleteView.as_view(), name='delete-news'),


    #tools
    path('tools/', ToolsView.as_view(), name='tools-list'),
    path('user/tools/<slug:slug>/', ToolsDetailView.as_view(), name='tools-detail'),

    # manager
    path('create/tools/', ToolsCreateView.as_view(), name='tools-create'),
    path('tools/<slug:slug>/', ToolsManagerDetailView.as_view(), name='tools-det'),

    path('list/tools/', ToolsListView.as_view(), name='list-tools'),
    path('delete/tools/<slug:slug>/', ToolsDeleteView.as_view(), name='delete-tools'),



    #skills
    path('skills/', SkillsView.as_view(), name='skills-list'),

    path('skills/<slug:slug>/', SkillsDetailView.as_view(), name='skills-detail'),

    # manager
    path('create/skills/', SkillsCreateView.as_view(), name='skills-create'),
    path('manager/skills/<slug:slug>/', SkillsManagerDetailView.as_view(), name='skills-det'),
    path('list/skills/', SkillsListView.as_view(), name='list-skills'),
    path('delete/skills/<slug:slug>/', SkillsDeleteView.as_view(), name='delete-skills'),

    ]