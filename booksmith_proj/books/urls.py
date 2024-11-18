from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing_page,name='landing_page'),
    path('search/', views.search_books, name='search_books'),
    path('products/<int:book_id>/', views.product_detail, name='product_detail'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('category/<str:category_name>/', views.category_books, name='category_books'),
    path('toggle-wishlist/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('add-to-wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('mark_discount_seen/<int:book_id>/', views.mark_discount_seen, name='mark_discount_seen'),
]
