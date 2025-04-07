from django.urls import path
from .views import (
IndexView, InfoContentView, HeroContentCreateView,
    HeroContentUpdateView,
    HeroSectionView,
    HowItWorksView,
    ServiceSectionView,
    HeroDeleteView,
    HeroListView,

StepListView, StepDetailView, StepCreateView, StepUpdateView, StepDeleteView,
ServiceListView,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView,
TestimonialSectionView,
TestimonialListView,
    TestimonialCreateView,
    TestimonialUpdateView,
    TestimonialDeleteView,
    TestimonialDetailView,
ContactSubmissionListView, ContactSubmissionDetailView,
SocialLinkListView,
    SocialLinkDetailView,
    SocialLinkDeleteView,
SocialLinkCreateView,

ErrorView
)

app_name = 'base'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('info/', InfoContentView.as_view(), name='infor-index'),

    path('error/', ErrorView.as_view(), name='error-page'),

    # Hero Content
    path('hero-content/create/', HeroContentCreateView.as_view(), name='hero_content_create'),
    path('hero-content/update/<int:pk>/', HeroContentUpdateView.as_view(), name='hero_content_update'),
    path('hero/list/', HeroListView.as_view(), name='hero_content_list'),
    path('hero-content/delete/<int:pk>/', HeroDeleteView.as_view(), name='hero_content_delete'),

    path("hero-section/", HeroSectionView.as_view(), name="hero-section"),
    path("how-it-works/", HowItWorksView.as_view(), name="how-it-works"),
    path("service-section/", ServiceSectionView.as_view(), name="service-section"),
    path("testimonial-section/", TestimonialSectionView.as_view(), name='testimonial-section'),

    path("steps/", StepListView.as_view(), name="step-list"),
    path("steps/create/", StepCreateView.as_view(), name="step-create"),
    path("steps/<slug:slug>/", StepDetailView.as_view(), name="step-detail"),

    path("steps/<slug:slug>/update/", StepUpdateView.as_view(), name="step-update"),
    path("steps/<slug:slug>/delete/", StepDeleteView.as_view(), name="step-delete"),

    path("service/list/", ServiceListView.as_view(), name="service-list"),
    path("services/create/", ServiceCreateView.as_view(), name="service-create"),
    path("services/update/<slug:slug>/", ServiceUpdateView.as_view(), name="service-update"),
    path("services/delete/<slug:slug>/", ServiceDeleteView.as_view(), name="service-delete"),

    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('testimonials/create/', TestimonialCreateView.as_view(), name='testimonial-create'),
    path('testimonials/<slug:slug>/', TestimonialDetailView.as_view(), name='testimonial-detail'),
    path('testimonials/<slug:slug>/update/', TestimonialUpdateView.as_view(), name='testimonial-update'),
    path('testimonials/<slug:slug>/delete/', TestimonialDeleteView.as_view(), name='testimonial-delete'),

    path('submissions/', ContactSubmissionListView.as_view(), name='contactsubmission-list'),
    path('submissions/<slug:slug>/', ContactSubmissionDetailView.as_view(), name='contactsubmission-detail'),

    path('social-links/create/', SocialLinkCreateView.as_view(), name='sociallink-create'),
    path('social-links/', SocialLinkListView.as_view(), name='sociallink-list'),
    path('social-links/<slug:slug>/', SocialLinkDetailView.as_view(), name='sociallink-detail'),
    path('social-links/<slug:slug>/delete/', SocialLinkDeleteView.as_view(), name='sociallink-delete'),

]