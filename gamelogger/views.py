from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout
import json
from requests import post
from django.contrib.auth.decorators import login_required

# def age_ratings_view(request):
#     # API request details
#     url = 'https://api.igdb.com/v4/age_ratings'
#     headers = {
#         'Client-ID': '5fx0c2tdp25zr3fuazhlqmwvezok4f',  # Replace with your actual Client ID
#         'Authorization': 'Bearer 9xs6a5rq9q9i37q84ca5w82uasrwt9'  # Replace with your actual access token
#     }
#     data = 'fields category,checksum,content_descriptions,rating,rating_cover_url,synopsis;'

#     # Make the request to the IGDB API
#     try:
#         response = post(url, headers=headers, data=data)

#         # Check if the response is successful (200 OK)
#         if response.status_code == 200:
#             ratings = response.json()  # Parse the JSON response
#         else:
#             ratings = {'error': 'Failed to fetch data from IGDB API.'}
#     except Exception as e:
#         ratings = {'error': str(e)}  # Handle any exceptions

#     # Pass the response data to the template
#     return render(request, 'age_ratings.html', {'ratings': ratings})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to the home page or another page
    return redirect('home')  # Redirect to the home page or another page if GET

def home(request):
    context = {
        'greeting': 'Welcome to the Home Page!',
        'user_count': 42,  # Example static data
    }
    return render(request, 'home.html', context)

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

@login_required
def profile_view(request):
    # You can pass user-specific data to the profile page
    user = request.user
    return render(request, 'profile.html', {'user': user})