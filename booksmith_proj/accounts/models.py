from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='profile_pics')
    bio = models.TextField(blank=True)  # Optional bio field
    bought_books = models.ManyToManyField(Book, blank=True, related_name="buyers")
    wishlist = models.ManyToManyField(Book, blank=True, related_name="wishlisted_by")
    seen_discounted_books = models.ManyToManyField(Book, related_name="seen_by", blank=True)


    def __str__(self):
        return self.user.username



#naghimo nako daan lance, ipahimo jud siya ni best friend...
# naa nay cart_view sa views.py nimo, adjust lng to your liking
# butngan sad nako profile view, kay sa accounts mani (di rana kailangan for now)
# and then naa nay carts.html sa accounts/cart.html nimo
# eh pa chuy2 nalang

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")  # Add related_name
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="cart_items")  # Add related_name
    quantity = models.PositiveIntegerField(default=1, editable=False)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"
    
class PaymentMethod(models.TextChoices):
    GCASH = 'gcash', 'GCash'
    PAYPAL = 'paypal', 'PayPal'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to user
    order_total = models.DecimalField(max_digits=10, decimal_places=2)  # The total price for the order
    total_saved = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Total savings from discount
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.GCASH
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # For PayPal/GCash transaction ID
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # For PayPal or GCash payment details
    paypal_email = models.EmailField(max_length=255, blank=True, null=True)
    gcash_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} by {self.user.username} - {self.payment_status}"

    def get_total_payment(self):
        return self.order_total - self.total_saved  # Calculate the final payment after savings