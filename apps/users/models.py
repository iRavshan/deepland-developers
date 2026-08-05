from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import json
import urllib.request   

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.CharField(max_length=500, blank=True, default='https://api.dicebear.com/7.x/bottts/svg?seed=Deepland')
    bio = models.TextField(blank=True, default='Deepland platformasida AI va Dasturlash bo\'yicha ta\'lim olmoqda.')
    is_verified = models.BooleanField(default=False, verbose_name="Tasdiqlangan foydalanuvchi")
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Foydalanuvchi profili'
        verbose_name_plural = 'Foydalanuvchilar profillari'
        

    def __str__(self):
        return self.user.username

    def is_online(self):
        limit = timezone.now() - timedelta(minutes=5)
        return self.user.sessions.filter(last_activity__gte=limit).exists()
    is_online.boolean = True
    is_online.short_description = 'Saytda (Online)'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    device_name = models.CharField(max_length=255, blank=True, null=True, help_text="Qurilma nomi (masalan, iPhone 13, Windows PC)")
    os_name = models.CharField(max_length=100, blank=True, null=True, help_text="Operatsion tizim")
    browser = models.CharField(max_length=100, blank=True, null=True, help_text="Brauzer nomi")
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="IP manzil")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Qurilma manzili (masalan, Toshkent, O'zbekiston)")
    session_key = models.CharField(max_length=40, blank=True, null=True, help_text="Django session kaliti")
    is_active = models.BooleanField(default=True, help_text="Sessiya faolmi?")
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_activity']
        verbose_name = 'Foydalanuvchi sessiyasi'
        verbose_name_plural = 'Foydalanuvchi sessiyalari'

    def __str__(self):
        device = self.device_name or "Noma'lum qurilma"
        return f"{self.user.username} - {device} ({self.ip_address})"

    def is_online(self):
        if not self.last_activity:
            return False
        limit = timezone.now() - timedelta(minutes=5)
        return self.last_activity >= limit
    is_online.boolean = True
    is_online.short_description = 'Saytda (Online)'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def parse_user_agent(user_agent):
    os_name = "Noma'lum OS"
    browser = "Noma'lum Brauzer"
    device_name = "Noma'lum Qurilma"

    if not user_agent:
        return device_name, os_name, browser

    ua_lower = user_agent.lower()
    
    if "windows" in ua_lower:
        os_name = "Windows"
        device_name = "Windows PC"
    elif "mac os" in ua_lower or "macintosh" in ua_lower:
        os_name = "macOS"
        device_name = "Mac"
    elif "android" in ua_lower:
        os_name = "Android"
        device_name = "Android Device"
    elif "iphone" in ua_lower:
        os_name = "iOS"
        device_name = "iPhone"
    elif "ipad" in ua_lower:
        os_name = "iOS"
        device_name = "iPad"
    elif "linux" in ua_lower:
        os_name = "Linux"
        device_name = "Linux PC"
        
    if "edg" in ua_lower:
        browser = "Edge"
    elif "chrome" in ua_lower and "edg" not in ua_lower:
        browser = "Chrome"
    elif "safari" in ua_lower and "chrome" not in ua_lower:
        browser = "Safari"
    elif "firefox" in ua_lower:
        browser = "Firefox"
    elif "opera" in ua_lower or "opr" in ua_lower:
        browser = "Opera"
        
    return device_name, os_name, browser

@receiver(user_logged_in)
def save_user_session(sender, request, user, **kwargs):
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    device_name, os_name, browser = parse_user_agent(user_agent)
    
    location = "Noma'lum"
    if ip_address and ip_address != '127.0.0.1':
        try:
            url = f"http://ip-api.com/json/{ip_address}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "success":
                    city = data.get("city", "")
                    country = data.get("country", "")
                    location = f"{city}, {country}".strip(', ')
        except Exception:
            pass
            
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        
    UserSession.objects.create(
        user=user,
        device_name=device_name,
        os_name=os_name,
        browser=browser,
        ip_address=ip_address,
        location=location,
        session_key=session_key,
    )
