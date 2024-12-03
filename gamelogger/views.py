from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout
import json
from requests import post
from django.contrib.auth.decorators import login_required
from .utils import fetch_all_igdb_games #sam
from django.core.paginator import Paginator
import logging
from members.models import Game
from asgiref.sync import sync_to_async
logger = logging.getLogger(__name__)

@sync_to_async
def render_async(request, template, context):
    return render(request, template, context)

@sync_to_async
def get_paginator(games, per_page):
    return Paginator(games, per_page)

@sync_to_async
def get_page(paginator, page_number):
    return paginator.get_page(page_number)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to the home page or another page
    return redirect('home')  # Redirect to the home page or another page if GET

def home(request):
    print("Home view has been triggered!")
    handpicked_game_ids = [10399, 136380, 33427, 186638, 131046, 109323]
    trending_games = Game.objects.filter(id__in=handpicked_game_ids)
    print(f"Trending games: {trending_games}")
    context = {
        'trending_games': trending_games,  # Pass handpicked games to template
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

async def game_list(request):
    try:
        # Fetch all games asynchronously
        games = await fetch_all_igdb_games(total_games=500)
    except Exception as e:
        logger.exception(f"Failed to fetch games: {e}")
        games = []

    # Paginate the games
    paginator = Paginator(games, 10)  # Display 10 games per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    is_authenticated = await sync_to_async(getattr)(request.user, 'is_authenticated', False)

    # Prepare context
    context = {
        'page_obj': page_obj,
        'is_authenticated': is_authenticated,  # Pass this to the template
    }

    # Render the template asynchronously
    response = await render_async(request, 'game_list.html', context)
    return response

@login_required
def profile_view(request):
    # You can pass user-specific data to the profile page
    user = request.user
    return render(request, 'profile.html', {'user': user})

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
