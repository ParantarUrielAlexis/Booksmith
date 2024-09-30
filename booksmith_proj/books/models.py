from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    # Create book ID primary key (Django creates it automatically unless specified otherwise)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30, default=None, blank=False)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default=None, blank=True)
    price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    discount_percent = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    image_url = models.CharField(max_length=2083, default='', blank=True)  # Can be empty
    thumbnail_image_url = models.CharField(max_length=2083, default='', blank=True)  # New field for thumbnail
    bestseller = models.BooleanField(default=False)  # Flag best sellers

    def discounted_price(self):
        """
        Calculate the final price after applying the discount.
        """
        if self.price is None:
            return None  # Handle case where price is not set
        discount_amount = (self.discount_percent / 100) * self.price
        return self.price - discount_amount

    def __str__(self):
        return self.title
