from django.contrib import admin
from .models import Course, Lesson, Unit, Category

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Unit)
admin.site.register(Category)