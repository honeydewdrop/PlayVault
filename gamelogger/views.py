from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or some other view
        else:
            # Handle invalid login
            pass
    return render(request, 'login.html')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        # Check if passwords match
        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Log the user in after registration
            login(request, user)

            return redirect('home')  # Redirect to home or wherever after registration
        else:
            # Handle case where passwords don't match
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'register.html')
