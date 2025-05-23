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
from django.db import IntegrityError
from .forms import ProfileUpdateForm
from .utils import convert_pdf_to_html
from .models import Payment
from decimal import Decimal

# Create your views here.
def home(request):

    return render(request, 'landing_page.html')


def signup(request):
    if request.method == "POST":
        # email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Email already exists.")
        #     return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        try:
            # Create the User
            myuser = User.objects.create_user(username=username, password=pass1)
            myuser.save()

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
            # Calculate the price considering discounts
            if item.book.discount_percent > 0:
                # Use discounted price if there's a discount
                price_per_unit = item.book.discounted_price()
            else:
                # Use the original price if no discount
                price_per_unit = item.book.price

            # Condition to check if the user wants more than 1
            new_price = price_per_unit * item.quantity

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




@login_required
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)

        # If no items in the cart, show a warning message and redirect to the cart page
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart')

        # Initialize total price and savings as Decimals
        total_price = Decimal('0.00')
        total_saved = Decimal('0.00')

        for item in cart_items:
            original_price = item.book.price
            if item.book.discount_percent > 0:
                price_per_unit = Decimal(item.book.discounted_price())  # Ensure it's a Decimal
                savings = (Decimal(original_price) - price_per_unit) * Decimal(item.quantity)  # Convert to Decimal
                total_saved += savings
            else:
                price_per_unit = Decimal(original_price)  # Convert to Decimal

            item.new_price = price_per_unit * Decimal(item.quantity)  # Ensure this is Decimal
            total_price += item.new_price  # Add as Decimal

        # Create a payment record (assuming this is only a dummy payment process for now)
        payment = Payment.objects.create(
            user=request.user,
            order_total=total_price,
            total_saved=total_saved,
            payment_method='gcash',  # Assuming default payment method as 'gcash'
            payment_status='Pending',
            transaction_id='',
            paypal_email=None,  # Set None as we're using 'gcash'
            gcash_number=None  # Set None as we're not processing payment details in this example
        )

        # Update payment status to 'Completed' after creation
        payment.payment_status = 'Completed'
        payment.save()

        # Prepare context to pass to the template
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_saved': total_saved,
            'cart_item_count': cart_items.count(),
        }

        return render(request, 'accounts/checkout.html', context)

    return redirect('login')




@login_required
def profile_view(request):
    user = request.user
    # Combined books for display
    all_books = user.profile.wishlist.all() | user.profile.bought_books.all()
    cart_item_count = 0
    cart_item_count = CartItem.objects.filter(user=request.user).count()
    context = {
        'user': user,
        'all_books': all_books,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'accounts/profile.html', context)


def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_authenticated"}, status=401)

    book = get_object_or_404(Book, pk=book_id)
    existing_cart_item = CartItem.objects.filter(user=request.user, book=book).first()

    if existing_cart_item:
        return JsonResponse({"error": "already_in_cart"}, status=200)

    # If not already in cart, add the item
    CartItem.objects.create(user=request.user, book=book)

    return JsonResponse({"success": "added_to_cart", "cart_item_count": CartItem.objects.filter(user=request.user).count()})


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

        # Calculate the subtotal by summing discounted prices when available
        subtotal = sum(
            (
                item.book.discounted_price() if item.book.discount_percent > 0 else item.book.price
            ) * item.quantity
            for item in CartItem.objects.filter(user=request.user)
        )

        # Use subtotal as the order total for now if there are no additional fees or calculations
        total_price = subtotal

        return JsonResponse({
            'message': f'Quantity {action}d successfully!',
            'new_quantity': cart_item.quantity,
            'subtotal': subtotal,
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



