from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from datetime import datetime
from .models import Profile, Cart
from books.views import landing_page
# Create your views here.
def home(request):
    return render(request, "landing_page")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Password does not match.")
            return redirect('signup')

        myuser = User.objects.create_user(username, email,pass1)
        myuser.save()

        messages.success(request, "Successfully Registered.")

        return redirect('signup')

    return render(request, "accounts/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully signed in!')
            return render(request, 'accounts/signin.html')

        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'accounts/signin.html')

    if request.user.is_authenticated:
        return redirect('landing_page')  # Redirect to the landing page or desired page

    return render(request, "accounts/signin.html")

def aboutus(request):
    return render(request, "aboutus.html")

def contactus(request):
    return render(request, "contactus.html")

def cart_view(request):
    # Fetch all cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)

    # Optionally, calculate the total price
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    # Pass the cart items and total price to the template
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user,  # Pass the logged-in user object to the template
    })
