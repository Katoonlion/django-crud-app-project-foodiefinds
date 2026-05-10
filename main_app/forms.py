from django.forms import ModelForm
from .models import Restaurant, UserRestaurant


# Create your views here.

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine', 'location', 'image_url']   

class UserRestaurantForm(ModelForm):
    class Meta:
        model = UserRestaurant
        fields = ['rating', 'review']