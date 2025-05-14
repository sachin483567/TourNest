from django.db import models
from django.contrib.auth.models import User

class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='host_profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_documents = models.FileField(upload_to='host_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Host specific fields
    company_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hosting_since = models.DateTimeField(auto_now_add=True)
    total_properties = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def update_property_count(self):
        self.total_properties = self.properties.count()  # Using related_name from Location model
        self.save()

    def update_average_rating(self):
        reviews = self.properties.all().values_list('reviews__rating', flat=True)
        if reviews:
            avg = sum(filter(None, reviews)) / len(list(filter(None, reviews)))
            self.average_rating = round(avg, 2)
            self.save()

    class Meta:
        ordering = ['-created_at']
