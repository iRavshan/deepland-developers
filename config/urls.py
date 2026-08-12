from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from config.sitemaps import StaticSitemap, CourseSitemap, LessonSitemap, ProjectSitemap

admin.site.site_header = "Deepland Developers"
admin.site.site_title = "Deepland Developers"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"

sitemaps = {
    'static': StaticSitemap,
    'courses': CourseSitemap,
    'lessons': LessonSitemap,
    'projects': ProjectSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.courses.urls')),
    path('', include('apps.users.urls')),
    path('projects/', include('apps.projects.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('humans.txt', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('llms.txt', TemplateView.as_view(template_name='llms.txt', content_type='text/plain')),
    path('mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'config.views.custom_404'
handler500 = 'config.views.custom_500'
handler403 = 'config.views.custom_403'
handler400 = 'config.views.custom_400'