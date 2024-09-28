from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .models import Profile
# Create your views here.

# this could conflict with your main page, so check
# this is not used btw
def home(request):
    return render(request, "accounts/index.html")

def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        birthdate = request.POST['birthdate']
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

        birthdate = datetime.strptime(request.POST['birthdate'], '%Y-%m-%d').date()
        today = datetime.today().date()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 18:
            messages.error(request, "Must be 18 plus")
            return redirect('signup')

        myuser = User.objects.create_user(username, email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        profile = Profile(user=myuser, gender=gender,birthdate=birthdate)
        profile.save()

        messages.success(request, "Successfully Registered.")


    return render(request, "accounts/signup.html")