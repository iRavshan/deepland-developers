from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.courses.models import Course, Lesson
from apps.projects.models import Project


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'course_list', 'learning_guide', 'projects:list']

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Course.objects.all()

    def location(self, obj):
        return reverse('course_detail', kwargs={'slug': obj.slug})


class LessonSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Lesson.objects.select_related('course').all()

    def location(self, obj):
        return reverse('lesson_detail', kwargs={
            'course_slug': obj.course.slug,
            'lesson_slug': obj.slug,
        })


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()
