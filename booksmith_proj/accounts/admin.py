from django.contrib import admin
from .models import Profile, CartItem, Payment
# Register your models here.

admin.site.register(Profile)
admin.site.register(CartItem)
admin.site.register(Payment)