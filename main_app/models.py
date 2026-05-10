from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = (
    ('want', 'Want to Try'),
    ('visited', 'Visited'),
)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class UserRestaurant(models.Model):
    STATUS_CHOICES = (
        ('want', 'Want to Try'),
        ('visited', 'Visited'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want')
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f'{self.user.username} - {self.restaurant.name}'