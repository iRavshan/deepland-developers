from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="code")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Kategoriya rasmi")
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
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name="Kurs rasmi")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration = models.CharField(max_length=50, default='10 soat')
    total_lessons = models.IntegerField(default=12)
    icon = models.CharField(max_length=50, default='book-open')
    color = models.CharField(max_length=20, default='blue')
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
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lessons', blank=True, null=True)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(blank=True, null=True, verbose_name="Tartib raqami")
    content = MDTextField(verbose_name="Kontent")
    duration = models.CharField(max_length=20, default='15 daqiqa')
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']

    def save(self, *args, **kwargs):
        skip_shift = kwargs.pop('skip_shift', False)
        
        if not self.order:
            from django.db.models import Max
            max_order = Lesson.objects.filter(course=self.course).aggregate(Max('order'))['order__max']
            self.order = (max_order or 0) + 1
        elif not skip_shift:
            if self.pk:
                old_order = Lesson.objects.get(pk=self.pk).order
                if old_order != self.order:
                    # Vaqtincha bazada conflict bo'lmasligi uchun chetga olib turamiz
                    temp_order = 999000 + self.pk
                    Lesson.objects.filter(pk=self.pk).update(order=temp_order)
                    
                    if self.order < old_order:
                        # Pastga surish (order + 1)
                        lessons_to_shift = Lesson.objects.filter(
                            course=self.course, order__gte=self.order, order__lt=old_order
                        ).exclude(id=self.id).order_by('-order')
                        for lesson in lessons_to_shift:
                            lesson.order += 1
                            lesson.save(skip_shift=True)
                    else:
                        # Yuqoriga surish (order - 1)
                        lessons_to_shift = Lesson.objects.filter(
                            course=self.course, order__gt=old_order, order__lte=self.order
                        ).exclude(id=self.id).order_by('order')
                        for lesson in lessons_to_shift:
                            lesson.order -= 1
                            lesson.save(skip_shift=True)
            else:
                if Lesson.objects.filter(course=self.course, order=self.order).exists():
                    lessons_to_shift = Lesson.objects.filter(
                        course=self.course, order__gte=self.order
                    ).order_by('-order')
                    for lesson in lessons_to_shift:
                        lesson.order += 1
                        lesson.save(skip_shift=True)
                    
        super().save(*args, **kwargs)

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

class LessonBookmark(models.Model):
    """Foydalanuvchilar darslarni saqlab qo'yishi uchun (Bookmark)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_bookmarks')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = "Saqlangan dars"
        verbose_name_plural = "Saqlangan darslar"

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"