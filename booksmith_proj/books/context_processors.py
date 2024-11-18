# myapp/context_processors.py
from .models import Book, Category

def categories_processor(request):
    # Fetch distinct category names from the Category model
    categories = Category.objects.values_list('name', flat=True).distinct()

    return {
        'categories': categories
    }

def discounted_wishlist_books(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        # Get wishlisted books with a discount
        wishlisted_books = profile.wishlist.filter(discount_percent__gt=0)

        # Remove books already seen from the list
        discounted_books = [
            book for book in wishlisted_books if book not in profile.seen_discounted_books.all()
        ]

        return {'discounted_books': discounted_books}
    return {'discounted_books': []}