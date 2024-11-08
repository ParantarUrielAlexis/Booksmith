from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing_page,name='landing_page'),
    path('search/', views.search_books, name='search_books'),
    path('products/<int:book_id>/', views.product_detail, name='product_detail'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('category/<str:category>/', views.category_books, name='category_books'),
]
