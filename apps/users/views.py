from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from apps.users.forms import CustomUserCreationForm

from apps.users.models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
        'profile_user': request.user,
    }
    return render(request, 'users/profile.html', context)

def public_profile_view(request, username):
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=target_user)
    context = {
        'profile': profile,
        'profile_user': target_user,
    }
    return render(request, 'users/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')
