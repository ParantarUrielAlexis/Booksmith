from django.db import models
from django.contrib.auth.models import User
from books.models import Book
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics', default='default_avatar.png')
    bio = models.TextField(blank=True)  # Optional bio field

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
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"
