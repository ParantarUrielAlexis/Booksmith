from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup,name='signup'),
    path('signin/', views.signin,name='signin'),
    path('aboutus/', views.aboutus,name='aboutus'),
    path('contactus/', views.contactus,name='contactus'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
]
