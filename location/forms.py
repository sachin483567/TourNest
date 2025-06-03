from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter property name'
        })
    )
    
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter location/address'
        })
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Describe your property',
            'rows': 4
        }),
        required=False
    )
    
    rent = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Price per night'
        })
    )
    
    capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Maximum guests'
        }),
        required=False
    )
    
    facilities = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'List amenities (e.g., WiFi, Pool, Kitchen, etc.)',
            'rows': 3
        }),
        required=False
    )
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'accept': 'image/*'
        }),
        required=False  # Make sure it's not required
    )
    
    latitude = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Latitude (optional)',
            'step': 'any'
        }),
        required=False
    )
    
    longitude = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Longitude (optional)',
            'step': 'any'
        }),
        required=False
    )

    class Meta:
        model = Location
        fields = ['name', 'location', 'description', 'rent', 'capacity', 'facilities', 'image', 'latitude', 'longitude']