from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Location, Booking
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q

def browse(request):
    # Get search parameters from request
    destination = request.GET.get('destination', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    amenities = request.GET.getlist('amenities')
    sort_by = request.GET.get('sort_by')
    
    # Search locations
    locations = Location.search_locations(
        destination=destination,
        min_price=min_price,
        max_price=max_price,
        amenities=amenities,
        sort_by=sort_by
    )
    
    context = {
        "locationList": locations,
        "search_params": {
            "destination": destination,
            "min_price": min_price,
            "max_price": max_price,
            "amenities": amenities,
            "sort_by": sort_by
        }
    }
    return render(request, "browse.html", context)

def productDetails(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    context ={
        "location":location
    }
    return render(request, "details.html", context=context)

@login_required
def create_booking(request, location_id):
    if request.method == 'POST':
        location = get_object_or_404(Location, id=location_id)
        
        # Get form data
        check_in = datetime.strptime(request.POST['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.POST['check_out'], '%Y-%m-%d').date()
        guests = int(request.POST['guests'])
        
        # Calculate total price
        nights = (check_out - check_in).days
        total_price = (location.rent * nights) + 500  # Adding service fee
        
        # Create booking
        booking = Booking.objects.create(
            location=location,
            user=request.user,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total_price=total_price,
            status='pending'
        )
        
        messages.success(request, 'Booking created successfully!')
        return redirect('booking_confirmation', booking_id=booking.id)
    
    return redirect('location_detail', location_id=location_id)

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'location': booking.location,
        'nights': (booking.check_out - booking.check_in).days,
    }
    return render(request, 'booking_confirmation.html', context)

@staff_member_required
def manage_bookings(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    bookings = Booking.objects.all().order_by('-created_at')
    
    # Apply filters
    if search_query:
        bookings = bookings.filter(
            Q(user__username__icontains=search_query) |
            Q(location__name__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookings': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Booking.STATUS_CHOICES,
    }
    return render(request, 'admin/manage_bookings.html', context)

@staff_member_required
def update_booking_status(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking #{booking.id} status updated to {new_status}')
        
    return redirect('manage_bookings')

