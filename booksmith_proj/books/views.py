from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review, Category, Author
from accounts.models import CartItem, Profile
from django.db.models import Q
from .forms import ReviewForm
import random
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def landing_page(request):
    books = list(Book.objects.all())
    featured_book = random.choice(books) if books else None

    if request.user.is_authenticated:
        # Exclude books that the user has already bought
        recommended_books = Book.objects.filter(recommended=True).exclude(
            id__in=request.user.profile.bought_books.values('id')
        ).order_by('?')[:4]
    else:
        # For unauthenticated users, recommend random books
        recommended_books = Book.objects.filter(recommended=True).order_by('?')[:4]

    best_sellers = Book.objects.filter(bestseller=True).order_by('?')  # Fetch best sellers

    # Fetch distinct category names
    categories = Category.objects.values_list('name', flat=True).distinct()

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
    search_results = Book.objects.filter(
        Q(title__icontains=query) | Q(author__name__icontains=query)
    ) if query else []
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

    average_rating = None
    if reviews.exists():
        total_rating = sum([review.rating for review in reviews if review.rating is not None])
        rating_count = sum([1 for review in reviews if review.rating is not None])
        if rating_count > 0:
            average_rating = round(total_rating / rating_count, 1)

    # Pass book, reviews, and similar_books to the template
    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
        'similar_books': similar_books,
        'cart_item_count': cart_item_count,
        'average_rating': average_rating,
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

def category_books(request, category_name):
    # Get the category object using category_name, or return 404 if not found
    category = get_object_or_404(Category, name=category_name)

    # Filter books by the category
    books = Book.objects.filter(category=category)

    # Render the books for the given category
    return render(request, 'category_books.html', {'books': books, 'category': category})


@login_required
def toggle_wishlist(request, book_id):
    profile = request.user.profile
    book = get_object_or_404(Book, id=book_id)

    if book in profile.wishlist.all():
        profile.wishlist.remove(book)
        return JsonResponse({'status': 'removed'})
    else:
        profile.wishlist.add(book)
        return JsonResponse({'status': 'added'})


@login_required
def add_to_wishlist(request, book_id):
    try:
        profile = Profile.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        profile.wishlist.add(book)
        profile.save()
        return JsonResponse({'message': 'Book added to wishlist'})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def mark_discount_seen(request, book_id):
    if request.user.is_authenticated:
        profile = request.user.profile
        book = get_object_or_404(Book, id=book_id)
        profile.seen_discounted_books.add(book)
    return redirect('product_detail', book_id=book_id)