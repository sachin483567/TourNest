# -*- encoding: utf-8 -*-

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Host
from .forms import LoginForm, RegisterForm, UserProfileForm, HostProfileForm


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('location:browse')  # Redirect if already logged in

    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "you are logged in")
                # Redirect to the URL specified in the 'next' parameter, or to home page
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                msg = 'Invalid credentials'
                messages.error(request, msg)
        else:
            msg = 'Error validating the form'
            messages.error(request, msg)

    return render(request, "login.html", {"form": form, "msg": msg})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('location:browse')


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('location:browse')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('authentication:login')
    else:
        form = RegisterForm()
        
    return render(request, 'authentication/register.html', {'form': form})

@login_required
def user_profile_view(request):
    """Display and update user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('authentication:user_profile')
    else:
        form = UserProfileForm(instance=request.user)
        
    context = {
        'form': form
    }
    return render(request, 'authentication/user_profile.html', context)

@login_required
def host_profile_view(request):
    """Display and update host profile"""
    try:
        host = request.user.host
    except Host.DoesNotExist:
        # Redirect to become host page if user is not a host
        return redirect('authentication:become_host')
    
    if request.method == 'POST':
        form = HostProfileForm(request.POST, request.FILES, instance=host)
        if form.is_valid():
            form.save()
            messages.success(request, 'Host profile updated successfully.')
            return redirect('authentication:host_profile')
    else:
        form = HostProfileForm(instance=host)
        
    context = {
        'form': form
    }
    return render(request, 'authentication/host_profile.html', context)

@login_required
def become_host_view(request):
    """Allow user to become a host"""
    # Check if user is already a host
    try:
        host = request.user.host
        messages.info(request, 'You are already registered as a host.')
        return redirect('authentication:host_profile')
    except Host.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = HostProfileForm(request.POST, request.FILES)
        if form.is_valid():
            host = form.save(commit=False)
            host.user = request.user
            host.save()
            messages.success(request, 'You are now registered as a host!')
            return redirect('authentication:host_profile')
    else:
        form = HostProfileForm()
        
    context = {
        'form': form
    }
    return render(request, 'authentication/become_host.html', context)
