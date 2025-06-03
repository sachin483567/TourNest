# -*- encoding: utf-8 -*-

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Host
from location.models import Location

from .forms import LoginForm, RegisterForm, UserProfileForm, HostProfileForm, HostSignUpForm  # Add HostSignUpForm to the import statement


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('location:browse')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('location:browse')


def register_user(request):  # This is the function being imported in urls.py
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('location:browse')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # Use RegisterForm instead of SignUpForm
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()  # Use RegisterForm instead of SignUpForm
        
    return render(request, 'authentication/register.html', {'form': form})


def register_host(request):
    """Handle host registration"""
    if request.method == 'POST':
        form = HostSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create host profile
            Host.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number')
            )
            messages.success(request, 'Host account created successfully!')
            return redirect('host_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HostSignUpForm()
    
    return render(request, 'become_host.html', {'form': form})


def host_login(request):
    """Handle host login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a host
            try:
                host = user.host
                login(request, user)
                return redirect('host_dashboard')
            except Host.DoesNotExist:
                messages.error(request, 'You are not registered as a host.')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'hostlogin.html')


@login_required
def host_dashboard(request):
    """Host dashboard view"""
    try:
        host = request.user.host
        # Get host's locations
        from location.models import Location, Booking
        from django.db.models import Sum
        
        # Fetch all locations owned by this host
        locations = Location.objects.filter(host=host)
        total_locations = locations.count()
        
        # Get active bookings
        active_bookings = Booking.objects.filter(
            location__host=host,
            status__in=['confirmed', 'active']
        ).count()
        
        # Calculate total earnings
        total_earnings = Booking.objects.filter(
            location__host=host,
            status='completed'
        ).aggregate(
            total=Sum('location__rent')
        )['total'] or 0
        
        context = {
            'host': host,
            'locations': locations,
            'total_locations': total_locations,
            'active_bookings': active_bookings,
            'total_earnings': total_earnings,
        }
        return render(request, 'host_dashboard.html', context)
    except Host.DoesNotExist:
        messages.error(request, 'You are not registered as a host.')
        return redirect('authentication:register_host')
