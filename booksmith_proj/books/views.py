from django.shortcuts import render
from .models import Book
from accounts.models import CartItem
import random

def landing_page(request):

    books = list(Book.objects.all())
    featured_book = random.choice(books) if books else None
    recommended_books = Book.objects.order_by('?')[:4]
    best_sellers = Book.objects.order_by('?').filter(bestseller=True)  # Fetch best sellers

    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
        
    context = {
        'featured_book': featured_book,
        'recommended_books': recommended_books,
        'best_sellers': best_sellers,  # Pass best sellers to template
        'is_authenticated': request.user.is_authenticated,
        'cart_item_count': cart_item_count,
    }

    return render(request, 'landing_page.html', context)



def search_books(request):
    query = request.GET.get('q')
    search_results = Book.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'search_results': search_results, 'query': query})
