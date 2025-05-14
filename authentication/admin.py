from django.contrib import admin
from .models import Host

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_verified', 'total_properties', 'average_rating', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'company_name')
    readonly_fields = ('created_at', 'updated_at', 'total_properties', 'average_rating')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'phone_number', 'address', 'profile_picture')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_documents')
        }),
        ('Host Details', {
            'fields': ('company_name', 'description')
        }),
        ('Statistics', {
            'fields': ('total_properties', 'average_rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
