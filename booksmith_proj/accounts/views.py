from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .models import Profile
# Create your views here.
def home(request):
    return render(request, "accounts/index.html")

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


    return render(request, "accounts/signup.html")

def aboutus(request):
    return render(request, "accounts/aboutus.html")