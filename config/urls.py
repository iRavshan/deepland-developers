from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.courses.urls')),
    path('', include('apps.users.urls')),
    path('humans.txt', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('llms.txt', TemplateView.as_view(template_name='llms.txt', content_type='text/plain')),
]

handler404 = 'config.views.custom_404'
handler500 = 'config.views.custom_500'
handler403 = 'config.views.custom_403'
handler400 = 'config.views.custom_400'