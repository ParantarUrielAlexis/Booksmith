# myapp/context_processors.py
from .models import Book

def categories_processor(request):
    categories = Book.objects.values_list('category', flat=True).distinct()
    return {
        'categories': categories
    }
