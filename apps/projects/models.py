from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Loyiha nomi")
    description = models.TextField(verbose_name="Loyiha haqida")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="Loyiha rasmi")
    github_link = models.URLField(blank=True, null=True, verbose_name="GitHub havolasi")
    live_link = models.URLField(blank=True, null=True, verbose_name="Jonli havola (Live link)")
    authors = models.ManyToManyField(User, related_name='projects', verbose_name="Mualliflar (Jamoa a'zolari)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Tahrirlangan vaqti")

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk})
