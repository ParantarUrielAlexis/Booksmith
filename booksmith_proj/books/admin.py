from django.contrib import admin
from .models import Book, Author, Category, Review
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Review)