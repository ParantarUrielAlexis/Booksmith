from django.shortcuts import render

# Create your views here.


# def home from accounts could conflict with your main page

def landing_page(request):
    return render(request, 'landing_page.html')