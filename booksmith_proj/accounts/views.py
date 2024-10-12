from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .models import Profile, Book, CartItem
from django.views.decorators.http import require_POST
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
    return render(request, "aboutus.html")

def contactus(request):
    return render(request, "contactus.html")

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.book.price * item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'accounts/cart.html', context)
    else:
        return redirect('login')



def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user,  
    })


@require_POST
def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)  
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'quantity': 1}  
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'message': 'Item added to cart!'})
    return JsonResponse({'error': 'User is not authenticated.'}, status=403)

def remove_from_cart(request, book_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, book__id=book_id, user=request.user)
        
        cart_item.delete()

        return JsonResponse({'success': True, 'message': 'Item removed from cart.'})
    
    return redirect('cart')