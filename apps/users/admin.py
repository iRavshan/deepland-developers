from django.contrib import admin
from .models import UserProfile, UserSession

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank_title', 'is_online')
    search_fields = ('user__username', 'rank_title')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_name', 'os_name', 'browser', 'ip_address', 'location', 'last_activity', 'is_online')
    list_filter = ('os_name', 'browser', 'is_active')
    search_fields = ('user__username', 'device_name', 'ip_address', 'location')
    readonly_fields = ('created_at', 'last_activity')