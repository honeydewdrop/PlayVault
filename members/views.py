from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .utils import fetch_all_igdb_games #sam
from django.core.paginator import Paginator
import logging
from .models import Game
from asgiref.sync import sync_to_async
logger = logging.getLogger(__name__)

@sync_to_async
def get_page(paginator, page_number):
    return paginator.get_page(page_number)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to the home page or another page
    return redirect('home')  # Redirect to the home page or another page if GET

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    context = {
        'greeting': 'Welcome to the Home Page!',
        'user_count': 42,  # Example static data
    }
    return render(request, 'home.html', context)


def game_list(request):
    games = Game.objects.all().order_by('-rating')  # Order by rating, highest first
    paginator = Paginator(games, 20)  # Show 20 games per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'members/game_list.html', {'page_obj': page_obj})

    # Paginate the games
    paginator = Paginator(games, 10)  # Display 10 games per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with paginated games
    return render(request, 'games.html', context={'page_obj': page_obj})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'profile.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import fetch_all_igdb_games  # Ensure this is imported
import logging
import asyncio

logger = logging.getLogger(__name__)

async def fetch_all_igdb_games_sync(total_games=500):
    """ Helper function to run the async function in a sync context. """
    return await fetch_all_igdb_games(total_games)

async def search(request):
    query = request.GET.get('q')
    results = []  # This will hold the search results

    if query:
        try:
            # Fetch all games asynchronously
            games = await fetch_all_igdb_games(total_games=500)  # Fetch games

            # Filter games based on the query
            results = [game for game in games if query.lower() in game['name'].lower()]
        except Exception as e:
            logger.exception(f"Failed to fetch games: {e}")
            results = []

    return render(request, 'search_results.html', {'results': results, 'query': query})
