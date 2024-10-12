from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30, default=None, blank=False)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default=None, blank=True)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    discount_percent = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    image_url = models.CharField(max_length=2083, default='', blank=True)
    thumbnail_image_url = models.CharField(max_length=2083, default='', blank=True)
    bestseller = models.BooleanField(default=False)

    def discounted_price(self):
        if self.price is None:
            return None
        discount_amount = (self.discount_percent / 100) * self.price
        return self.price - discount_amount

    def __str__(self):
        return self.title
