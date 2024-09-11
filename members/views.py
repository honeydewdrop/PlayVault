from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def login_user(request):
    return render(request, 'authenticate/login.html', {})
def register_user(request):
    return render(request, 'authenticate/register.html', {})
def home(request):
    return render(request, 'home.html', {})

# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Log the user in after registration
            login(request, user)

            return redirect('home')  # Redirect to the home page or another page
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'register.html')

def home(request):
    # Example data to pass to the template
    context = {
        'greeting': 'Welcome to the Home Page!',
        'user_count': 42,  # Example static data
        # You can also pass dynamic data, e.g., from a database
    }
    return render(request, 'home.html', context)