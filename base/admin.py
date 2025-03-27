from django.contrib import admin
from .models import SocialLink

@admin.register(SocialLink)

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'slug', 'url', 'created_at')
    prepopulated_fields = {'slug': ('platform',)}
    readonly_fields = ('created_at',)
    search_fields = ('platform', 'url', 'slug')
    list_filter = ('platform', 'created_at')