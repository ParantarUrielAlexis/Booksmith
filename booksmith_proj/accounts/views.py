from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .models import Profile, Book, CartItem
from django.views.decorators.http import require_POST
from books.views import landing_page
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
# Create your views here.
def home(request):
    return render(request, "landing_page")

from django.db import IntegrityError

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        gender = request.POST.get('gender')  # Get gender from the form
        birthdate = request.POST.get('birthdate')  # Get birthdate from the form

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        try:
            # Create the User
            myuser = User.objects.create_user(username=username, email=email, password=pass1)
            myuser.save()

            # Check if the profile already exists to avoid duplicate creation
            if not Profile.objects.filter(user=myuser).exists():
                Profile.objects.create(user=myuser, gender=gender, birthdate=birthdate)

            # Display a success message when the user and profile are created successfully
            messages.success(request, "Successfully Registered.")
            return redirect('signup')

        except IntegrityError as e:
            # Handle IntegrityError if profile or user creation fails
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    if request.user.is_authenticated:
        return redirect('landing_page')

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
        return redirect('landing_page')


    return render(request, "accounts/signin.html")

def aboutus(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()

        context = {
            'cart_item_count': cart_item_count
        }
        return render(request, 'aboutus.html', context)
    return render(request, "aboutus.html")

def contactus(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
        context = {
            'cart_item_count': cart_item_count
        }
        return render(request, 'contactus.html', context)
    return render(request, "contactus.html")

def cart_view(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.book.price * item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_item_count': cart_item_count
        }
        return render(request, 'accounts/cart.html', context)
    else:
        return redirect('login')



def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })


@require_POST
@require_POST
def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(id=book_id)  # Get the book based on the ID
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found.'}, status=404)

        # Check if the cart item already exists for the user and this book
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'quantity': 1}  # Set default quantity if a new cart item is created
        )

        if not created:
            # If the cart item already exists, return an error message
            return JsonResponse({'error': 'Already in the cart.'}, status=400)

        # Calculate the updated cart item count
        cart_item_count = CartItem.objects.filter(user=request.user).count()

        # If the item is newly created, return a success message along with the cart count
        return JsonResponse({'message': 'Item added to cart!', 'cart_item_count': cart_item_count})

    return JsonResponse({'error': 'User is not authenticated.'}, status=403)



def remove_from_cart(request, book_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, book__id=book_id, user=request.user)

        cart_item.delete()

        return JsonResponse({'success': True, 'message': 'Item removed from cart.'})

    return redirect('cart')


@login_required
def update_profile(request):
    profile = request.user.profile  # Get the current user's profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile data
            return redirect('profile_view')  # Redirect to the profile page after successful update
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/update_profile_picture.html', {'form': form, 'profile': profile})
