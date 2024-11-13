from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from accounts.models import CartItem
from django.db.models import Q
from .forms import ReviewForm
import random

def landing_page(request):
    books = list(Book.objects.all())
    featured_book = random.choice(books) if books else None
    recommended_books = Book.objects.order_by('?')[:4]
    best_sellers = Book.objects.filter(bestseller=True).order_by('?')  # Fetch best sellers
    categories = Book.objects.values_list('category', flat=True).distinct()

    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()

    context = {
        'featured_book': featured_book,
        'recommended_books': recommended_books,
        'best_sellers': best_sellers,
        'categories': categories,
        'is_authenticated': request.user.is_authenticated,
        'cart_item_count': cart_item_count,
    }

    return render(request, 'landing_page.html', context)

def search_books(request):
    query = request.GET.get('q')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) if query else []
    return render(request, 'search_results.html', {'search_results': search_results, 'query': query})

def product_detail(request, book_id):
    # Fetch the book based on the provided book ID
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()

    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.filter(parent__isnull=True)  # Get only top-level reviews (no replies)
    similar_books = Book.objects.exclude(pk=book_id)[:4]  # Get similar books

    form = ReviewForm()
    
    # Handle review form submission
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect("product_detail", book_id=book.id)
        else:
            return redirect("login")  # Redirect unauthenticated users to login page
    else:
        form = ReviewForm()

    # Pass book, reviews, and similar_books to the template
    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
        'similar_books': similar_books,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'product_detail.html', context)


def delete_review(request, review_id):
    # Fetch the review object
    review = get_object_or_404(Review, pk=review_id)

    # Check if the logged-in user is the owner of the review
    if review.user == request.user:
        review.delete()  # Delete the specific review from the database
        return redirect('product_detail', book_id=review.book.id)  # Redirect to the product detail page with the correct book ID

    # If the user is not the owner, redirect to product detail
    return redirect('product_detail', book_id=review.book.id)

def category_books(request, category):
    books = Book.objects.filter(category=category)  # Filter books by the category
    return render(request, 'category_books.html', {'books': books, 'category': category})
