from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import UserProfile, UserSession

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil ma\'lumotlari'
    fields = ('is_verified', 'avatar_url', 'bio', 'github_url', 'linkedin_url')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_verified')
    list_editable = ('first_name', 'last_name')
    
    def get_is_verified(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.is_verified
        return False
    get_is_verified.short_description = 'Verified'
    get_is_verified.boolean = True

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class UserProfileAdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="Ism")
    last_name = forms.CharField(max_length=30, required=False, label="Familiya")

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    list_display = ('user', 'get_first_name', 'get_last_name', 'is_verified', 'is_online')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_editable = ('is_verified',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.user.first_name = form.cleaned_data.get('first_name', '')
        obj.user.last_name = form.cleaned_data.get('last_name', '')
        obj.user.save(update_fields=['first_name', 'last_name'])

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Ism'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Familiya'

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_name', 'os_name', 'browser', 'ip_address', 'location', 'last_activity', 'is_online')
    list_filter = ('os_name', 'browser', 'is_active')
    search_fields = ('user__username', 'device_name', 'ip_address', 'location')
    readonly_fields = ('created_at', 'last_activity')