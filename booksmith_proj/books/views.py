from django.shortcuts import render, get_object_or_404
from .models import Book
from accounts.models import CartItem
from django.db.models import Q
import random

def landing_page(request):

    books = list(Book.objects.all())
    featured_book = random.choice(books) if books else None
    recommended_books = Book.objects.order_by('?')[:4]
    best_sellers = Book.objects.order_by('?').filter(bestseller=True)  # Fetch best sellers
    # Get distinct categories from the Book model
    categories = Book.objects.values_list('category', flat=True).distinct()

    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()

    context = {
        'featured_book': featured_book,
        'recommended_books': recommended_books,
        'best_sellers': best_sellers,  # Pass best sellers to template
        'categories': categories,  # Include categories in the context
        'is_authenticated': request.user.is_authenticated,
        'cart_item_count': cart_item_count,
    }

    return render(request, 'landing_page.html', context)



def search_books(request):
    query = request.GET.get('q')
    if query:
        # Use Q objects to filter by title OR author
        search_results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        search_results = []
    return render(request, 'search_results.html', {'search_results': search_results, 'query': query})

def product_detail(request, book_id):
    # Fetch the book based on the provided book ID
    book = get_object_or_404(Book, pk=book_id)

    # Fetch similar products, excluding the current one
    similar_books = Book.objects.exclude(pk=book_id)[:4]  # Limit to 4 similar products

    # Pass book and similar_books to the template
    context = {
        'book': book,
        'similar_books': similar_books,
    }
    return render(request, 'product_detail.html', context)

def category_books(request, category):
    books = Book.objects.filter(category=category)  # Filter books by the category
    return render(request, 'category_books.html', {'books': books, 'category': category})





