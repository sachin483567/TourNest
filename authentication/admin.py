from django.contrib import admin
from .models import Host

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']
    list_filter = ['user__date_joined']
    search_fields = ['user__username', 'user__email', 'phone_number']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Host Details', {
            'fields': ('bio', 'phone_number', 'profile_picture')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ['user']  # Make user field readonly when editing
        return []
