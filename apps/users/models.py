from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.CharField(max_length=500, blank=True, default='https://api.dicebear.com/7.x/bottts/svg?seed=Deepland')
    bio = models.TextField(blank=True, default='Deepland platformasida AI va Dasturlash bo\'yicha ta\'lim olmoqda.')
    xp_points = models.IntegerField(default=1500)
    solved_challenges_count = models.IntegerField(default=12)
    rank_title = models.CharField(max_length=100, default='AI Researcher')
    github_url = models.URLField(blank=True, default='https://github.com')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
