# Create your models here.
from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.IntegerField()
    rent = models.IntegerField()
    distance = models.IntegerField()
    location = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    facilities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def _str_(self):
        return self.name 
