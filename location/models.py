# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    rent = models.IntegerField()
    distance = models.IntegerField()
    location = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    facilities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    @classmethod
    def search_locations(cls, **kwargs):
        queryset = cls.objects.all()
        
        # Search by destination
        if kwargs.get('destination'):
            queryset = queryset.filter(location__icontains=kwargs['destination'])
        
        # Filter by price range
        if kwargs.get('min_price'):
            queryset = queryset.filter(rent__gte=kwargs['min_price'])
        if kwargs.get('max_price'):
            queryset = queryset.filter(rent__lte=kwargs['max_price'])
        
        # Filter by amenities
        if kwargs.get('amenities'):
            for amenity in kwargs['amenities']:
                queryset = queryset.filter(facilities__icontains=amenity)
        
        # Sort results
        sort_by = kwargs.get('sort_by', 'rent')
        if sort_by == 'price_low':
            queryset = queryset.order_by('rent')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-rent')
        
        return queryset

    def _str_(self):
        return self.name

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['location', 'user']  # One review per user per location

    def __str__(self):
        return f'{self.user.username}\'s review for {self.location.name}'

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Booking for {self.location.name} by {self.user.username}'
