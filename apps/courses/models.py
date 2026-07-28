from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="code")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
        
class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration = models.CharField(max_length=50, default='10 soat')
    total_lessons = models.IntegerField(default=12)
    rating = models.FloatField(default=4.9)
    icon = models.CharField(max_length=50, default='book-open')
    color = models.CharField(max_length=20, default='blue')
    duration = models.CharField(max_length=50, default='10 Hours')
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
    def total_lessons(self):
        return Lesson.objects.filter(unit__course=self).count()
    
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'slug']

    def __str__(self):
        return f"{self.course.title} — {self.title}"
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    content = MDTextField(verbose_name="Kontent")
    duration = models.CharField(max_length=20, default='15 daqiqa')
    duration = models.CharField(max_length=20, default='15 mins')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class LessonCompletion(models.Model):
    """Foydalanuvchi qaysi darsni tugatganini kuzatish uchun."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = "Tugatilgan dars"
        verbose_name_plural = "Tugatilgan darslar"

    def __str__(self):
        return f"{self.user.username} — {self.lesson.title}"

class LessonFeedback(models.Model):
    """Foydalanuvchilar darslarga bergan baholari (layk yoki dizlayk)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_feedbacks')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='feedbacks')
    is_helpful = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = "Darsga bildirilgan fikr"
        verbose_name_plural = "Darsga bildirilgan fikrlar"

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({'Foydali' if self.is_helpful else 'Foydasiz'})"