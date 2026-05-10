from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import Restaurant, UserRestaurant
from .forms import RestaurantForm, UserRestaurantForm

# Create your views here.

from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('restaurant-index')

    return render(request, 'home.html')


def restaurant_index(request):
    status = request.GET.get('status')
    restaurant_cards = []

    if request.user.is_authenticated and status:
        user_restaurants = UserRestaurant.objects.filter(
            user=request.user,
            status=status
        )

        for user_restaurant in user_restaurants:
            restaurant_cards.append({
                'restaurant': user_restaurant.restaurant,
                'user_restaurant': user_restaurant
            })
    else:
        restaurants = Restaurant.objects.all()

        for restaurant in restaurants:
            user_restaurant = None

            if request.user.is_authenticated:
                user_restaurant = UserRestaurant.objects.filter(
                    user=request.user,
                    restaurant=restaurant
                ).first()

            restaurant_cards.append({
                'restaurant': restaurant,
                'user_restaurant': user_restaurant
            })

    return render(request, 'restaurants/index.html', {
        'restaurant_cards': restaurant_cards,
        'status': status
    })



def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    user_restaurant = None

    if request.user.is_authenticated:
        user_restaurant = UserRestaurant.objects.filter(
            user=request.user,
            restaurant=restaurant
        ).first()

    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant,
        'user_restaurant': user_restaurant
    })


@login_required
def restaurant_create(request):
    restaurant_form = RestaurantForm(request.POST or None)
    review_form = UserRestaurantForm(request.POST or None)

    if restaurant_form.is_valid() and review_form.is_valid():
        new_restaurant = restaurant_form.save(commit=False)
        new_restaurant.user = request.user
        new_restaurant.save()

        user_restaurant = review_form.save(commit=False)
        user_restaurant.user = request.user
        user_restaurant.restaurant = new_restaurant
        user_restaurant.status = 'visited'
        user_restaurant.save()

        return redirect('restaurant-detail', restaurant_id=new_restaurant.id)

    return render(request, 'restaurants/form.html', {
        'restaurant_form': restaurant_form,
        'review_form': review_form
    })


@login_required
def restaurant_update(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if restaurant.user != request.user:
        return HttpResponseForbidden('You are not allowed to edit this restaurant.')

    user_restaurant, created = UserRestaurant.objects.get_or_create(
        user=request.user,
        restaurant=restaurant,
        defaults={'status': 'visited'}
    )

    restaurant_form = RestaurantForm(request.POST or None, instance=restaurant)
    review_form = UserRestaurantForm(request.POST or None, instance=user_restaurant)

    if restaurant_form.is_valid() and review_form.is_valid():
        restaurant_form.save()
        review_form.save()

        return redirect('restaurant-detail', restaurant_id=restaurant.id)

    return render(request, 'restaurants/form.html', {
        'restaurant_form': restaurant_form,
        'review_form': review_form,
        'restaurant': restaurant
    })


@login_required
def restaurant_delete(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if restaurant.user != request.user:
        return HttpResponseForbidden('You are not allowed to delete this restaurant.')

    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant-index')

    return render(request, 'restaurants/confirm_delete.html', {'restaurant': restaurant})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('restaurant-index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def my_list(request):
    status = request.GET.get('status')

    if status:
        user_restaurants = UserRestaurant.objects.filter(
            user=request.user,
            status=status
        )
    else:
        user_restaurants = UserRestaurant.objects.filter(user=request.user)

    return render(request, 'restaurants/my_list.html', {
        'user_restaurants': user_restaurants,
        'status': status
    })


@login_required
def update_user_restaurant_status(request, restaurant_id, status):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    user_restaurant, created = UserRestaurant.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )

    user_restaurant.status = status
    user_restaurant.save()

    return redirect('restaurant-detail', restaurant_id=restaurant.id)


@login_required
def user_restaurant_review(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    user_restaurant, created = UserRestaurant.objects.get_or_create(
        user=request.user,
        restaurant=restaurant,
        defaults={'status': 'visited'}
    )

    user_restaurant.status = 'visited'

    form = UserRestaurantForm(request.POST or None, instance=user_restaurant)

    if form.is_valid():
        form.save()
        return redirect('restaurant-detail', restaurant_id=restaurant.id)

    return render(request, 'restaurants/review_form.html', {
        'form': form,
        'restaurant': restaurant
    })


@login_required
def toggle_status(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    user_restaurant, created = UserRestaurant.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )

    if user_restaurant.status == 'visited':
        user_restaurant.status = 'want'
    else:
        user_restaurant.status = 'visited'

    user_restaurant.save()

    return redirect('restaurant-detail', restaurant_id=restaurant.id)