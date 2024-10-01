from django.db import models
from django.contrib.auth.models import User
from books.models import Book
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    birthdate = models.DateField()
    image = models.ImageField(upload_to='profile_pics', default='default_avatar.png')

    def __str__(self):
        return self.user.username

#naghimo nako daan lance, ipahimo jud siya ni best friend...
# naa nay cart_view sa views.py nimo, adjust lng to your liking
# butngan sad nako profile view, kay sa accounts mani (di rana kailangan for now)
# and then naa nay carts.html sa accounts/cart.html nimo
# eh pa chuy2 nalang
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link cart to user
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Link the book
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart item: {self.book.title}"