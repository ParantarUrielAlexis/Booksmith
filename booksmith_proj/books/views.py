from django.shortcuts import render
from .models import Book

def landing_page(request):
    # Get a featured book (e.g., the first book or a random one)
    featured_book = Book.objects.first()  # Or use `random()` or any filtering logic
    recommended_books = Book.objects.all()[:4]  # Example to get 4 recommended books
    best_sellers = Book.objects.filter(bestseller=True)  # Fetch best sellers

    context = {
        'featured_book': featured_book,
        'recommended_books': recommended_books,
        'best_sellers': best_sellers,  # Pass best sellers to template
    }

    return render(request, 'landing_page.html', context)
