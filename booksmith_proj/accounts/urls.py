from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import profile_view, update_profile

urlpatterns = [
    path('signup/', views.signup,name='signup'),
    path('signin/', views.signin,name='signin'),
    path('aboutus/', views.aboutus,name='aboutus'),
    path('contactus/', views.contactus,name='contactus'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', update_profile, name='update_profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('update_cart_quantity/<int:book_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
