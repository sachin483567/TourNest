from django.contrib import admin
from .models import Location, Review, Booking

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rent', 'distance', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('name', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('location', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('location__name', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'user', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('location__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('status',)