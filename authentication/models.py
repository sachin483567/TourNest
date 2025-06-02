from django.db import models
from django.contrib.auth.models import User

class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='hosts/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Host Profile"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def rating(self):
        # Calculate average rating across all properties
        from location.models import Review
        reviews = Review.objects.filter(location__host=self)
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0

    class Meta:
        ordering = ['-date_joined']
