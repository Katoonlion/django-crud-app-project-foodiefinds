"""
URL configuration for foodiefinds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_index, name='restaurant-index'),
    path('restaurants/create/', views.restaurant_create, name='restaurant-create'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/edit/', views.restaurant_update, name='restaurant-update'),
    path('restaurants/<int:restaurant_id>/delete/', views.restaurant_delete, name='restaurant-delete'),
    path('restaurants/<int:restaurant_id>/status/<str:status>/', views.update_user_restaurant_status,name='update-user-restaurant-status'),
    path('restaurants/<int:restaurant_id>/review/', views.user_restaurant_review,name='user-restaurant-review'),
    path('restaurants/<int:restaurant_id>/toggle/', views.toggle_status, name='toggle-status'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),

    path('restaurants/my-list/', views.my_list, name='my-list'),
    
    
]
