from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'authors__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_authors(self, obj):
        return ", ".join([user.username for user in obj.authors.all()])
    get_authors.short_description = 'Mualliflar'

