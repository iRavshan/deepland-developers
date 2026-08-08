import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Ism")
    last_name = forms.CharField(max_length=30, required=True, label="Familiya")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
            if len(username) <= 5:
                raise forms.ValidationError("Foydalanuvchi nomi 5 ta belgidan ko'p bo'lishi kerak.")
            if not re.match(r'^[a-z0-9_\.]+$', username):
                raise forms.ValidationError("Foydalanuvchi nomi faqat harflar, sonlar, pastki chiziq (_) va nuqtadan (.) iborat bo'lishi mumkin.")
            if '..' in username:
                raise forms.ValidationError("Foydalanuvchi nomida ikkita nuqta yonma-yon kelishi mumkin emas.")
            
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError("Bu foydalanuvchi nomi allaqachon band. Iltimos, boshqasini tanlang.")
            
            self.cleaned_data['username'] = username
        return username
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
        return user
