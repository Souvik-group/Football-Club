from django.contrib import admin
from .models import News, Media, Announcement, Event
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.conf import settings


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'uploaded_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'is_active', 'created_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'date', 'venue')



class CustomAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.email == settings.ADMIN_EMAIL

admin_site = CustomAdminSite(name='custom_admin')