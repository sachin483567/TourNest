# -*- encoding: utf-8 -*-

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Host
from location.models import Location

from .forms import LoginForm, SignUpForm, HostSignUpForm


def login_view(request):
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
                return redirect("/")
            else:
                msg = 'Invalid credentials'
                messages.error(request, msg)
        else:
            msg = 'Error validating the form'
            messages.error(request, msg)

    return render(request, "login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created - please <a href="/login">login</a>.'
            success = True
            messages.success(request, msg)
            return redirect("/login/")

        else:
            msg = 'Forms details are invalid'
            messages.error(request, msg)
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form, "msg": msg, "success": success})


def register_host(request):
    if request.method == 'POST':
        form = HostSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Use email as username
            user.save()
            
            # Create Host profile
            Host.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            
            messages.success(request, 'Your host account has been created successfully!')
            return redirect('property_details')
    else:
        form = HostSignUpForm()
    
    return render(request, 'become_host.html', {'form': form})

def host_login(request):  # Removed @login_required decorator
    # Redirect if already logged in as host
    if request.user.is_authenticated and hasattr(request.user, 'host'):
        return redirect('host_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and hasattr(user, 'host'):
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('host_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a host account.')
    
    return render(request, 'hostlogin.html')

@login_required
def host_dashboard(request):
    # Get host's locations
    locations = Location.objects.filter(host=request.user.host)
    
    # Get booking stats
    total_locations = locations.count()
    active_bookings = sum(location.booking_set.filter(status='confirmed').count() for location in locations)
    total_earnings = sum(location.booking_set.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0)
    
    context = {
        'locations': locations,
        'total_locations': total_locations,
        'active_bookings': active_bookings,
        'total_earnings': total_earnings,
    }
    return render(request, 'host_dashboard.html', context)
