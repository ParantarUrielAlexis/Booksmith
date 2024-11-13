from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


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
    pdf_file = models.FileField(upload_to='pdf_files/', null=True, blank=True)  # Store PDF files


    def discounted_price(self):
        if self.price is None:
            return None
        discount_amount = (self.discount_percent / 100) * self.price
        return self.price - discount_amount

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        return f'{self.user.username} - {self.comment[:20]}'