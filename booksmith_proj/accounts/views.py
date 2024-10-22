from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .models import Profile, Book, CartItem
from django.views.decorators.http import require_POST
from books.views import landing_page
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .utils import convert_pdf_to_html  # Import your utility function

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
        cart_items = CartItem.objects.filter(user=request.user)
        cart_item_count = cart_items.count()

        # Initialize total price
        total_price = 0

        # Loop through each cart item to calculate new price
        for item in cart_items:
            # Condition to check if the user wants more than 1
            if item.quantity > 1:
                new_price = item.book.price * item.quantity
            else:
                new_price = item.book.price
            
            # Add this new price to the total
            total_price += new_price

            # Assign new_price to the item to use it in the template
            item.new_price = new_price

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_item_count': cart_item_count
        }
        return render(request, 'accounts/cart.html', context)
    else:
        return redirect('login')



from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    # Handle POST request for payment submission
    if request.method == 'POST':
        payment_method = request.POST.get('payment')
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        expiry = request.POST.get('expiry')
        cvv = request.POST.get('cvv')

        # Add logic here for processing the payment
        # Redirect to success page after payment processing
        return redirect('payment_success')

    # Context to pass to the template
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_item_count = cart_items.count()

        # Initialize total price
        total_price = 0

        # Loop through each cart item to calculate new price
        for item in cart_items:
            # Calculate new price based on quantity
            item.new_price = item.book.price * item.quantity
            total_price += item.new_price  # Add to total price

        # Prepare context with cart items and total price
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_item_count': cart_item_count
        }

        return render(request, 'accounts/checkout.html', context)

    # Redirect to login page if user is not authenticated
    return redirect('login')



def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })


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
            # If the cart item already exists, increase the quantity
            cart_item.quantity += 1
            cart_item.save()

        # Calculate the updated cart item count
        cart_item_count = CartItem.objects.filter(user=request.user).count()

        # Return a success message along with the updated cart count
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


@require_POST
def update_cart_quantity(request, book_id, action):
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(user=request.user, book_id=book_id)
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found in the cart.'}, status=404)

        # Check the action (increase or decrease)
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                return JsonResponse({'error': 'Quantity cannot be less than 1.'}, status=400)

        cart_item.save()

        # Recalculate the total price after the update
        total_price = sum(item.book.price * item.quantity for item in CartItem.objects.filter(user=request.user))

        return JsonResponse({
            'message': f'Quantity {action}d successfully!',
            'new_quantity': cart_item.quantity,
            'total_price': total_price
        })

    return JsonResponse({'error': 'User not authenticated.'}, status=403)



@login_required
@csrf_exempt
def confirm_payment(request):
    if request.method == "POST":
        # Assuming you're passing cart items and total from your frontend
        cart_items = CartItem.objects.filter(user=request.user)

        # Add the books from the cart to the user's profile
        profile = Profile.objects.get(user=request.user)
        for item in cart_items:
            profile.bought_books.add(item.book)

        # Clear the cart
        cart_items.delete()

        # Redirect to profile page or a success page
        return redirect('profile_view')  # Make sure you have a 'profile' view and URL
    return render(request, 'checkout.html')





def read_book(request, book_id):
    book = Book.objects.get(id=book_id)
    html_content = ""

    if book.pdf_file:
        pdf_path = book.pdf_file.path  # Path to the PDF file
        html_content = convert_pdf_to_html(pdf_path)

    return render(request, 'accounts/read_book.html', {'book': book, 'html_content': html_content})



