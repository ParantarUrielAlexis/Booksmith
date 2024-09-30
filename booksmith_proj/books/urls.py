from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing_page,name='landing_page'),
    path('search/', views.search_books, name='search_books'),
]
