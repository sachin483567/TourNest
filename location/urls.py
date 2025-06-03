from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import browse, productDetails, create_booking, booking_confirmation
from . import views

app_name = 'location'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('browse/', browse, name='browse'),
    path("details/<int:location_id>", productDetails, name="locationDetails"),
    path('booking/create/<int:location_id>/', create_booking, name='create_booking'),
    path('booking/confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('admin/bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin/bookings/<int:booking_id>/update/', views.update_booking_status, name='update_booking_status'),
    path('location/<int:location_id>/review/', views.add_review, name='add_review'),
    path('host/bookings/', views.host_bookings, name='host_bookings'),

    # Host location management URLs
    path('add/', views.add_location, name='add_location'),
    path('<int:location_id>/edit/', views.edit_location, name='edit_location'),
    path('<int:location_id>/delete/', views.delete_location, name='delete_location'),
    path('<int:location_id>/toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('<int:location_id>/bookings/', views.location_bookings, name='location_bookings'),
]