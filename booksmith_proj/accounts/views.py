from django.shortcuts import render
# Create your views here.
def home(request):
    return render(request, "accounts/index.html")

def signup(request):
    return render(request, "accounts/signup.html")