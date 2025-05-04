from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import browse, productDetails, create_booking, booking_confirmation
from . import views

urlpatterns = [
    path('browse/', browse, name='browse'),
    path("details/<int:location_id>", productDetails, name="locationDetails"),
    path('booking/create/<int:location_id>/', create_booking, name='create_booking'),
    path('booking/confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('admin/bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin/bookings/<int:booking_id>/update/', views.update_booking_status, name='update_booking_status'),
]