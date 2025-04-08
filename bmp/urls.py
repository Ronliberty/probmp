from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('custom_account/', include('custom_account.urls')),

    path('chat/', include('chat.urls')),
    path('freelance/', include('freelance.urls')),
    path('partner/', include('partner.urls')),
    path('payment/', include('payment.urls')),
    path('service/', include('service.urls')),
    path('agents/', include('agents.urls')),
    path('accounts/', include('allauth.urls')),
path('logout/', LogoutView.as_view(), name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)