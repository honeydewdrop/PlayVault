from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.db import connection
from members.models import Profile
from .utils import fetch_all_igdb_games #sam
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from django.db.models import Avg, Count
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
    total_games = Game.objects.count()
    avg_rating = Game.objects.aggregate(Avg('rating'))['rating__avg']
    top_genres = Game.objects.values('genre').annotate(count=Count('id')).order_by('-count')[:5]
    recent_games = Game.objects.order_by('-release_date')[:10]
    
    context = {
        'total_games': total_games,
        'avg_rating': avg_rating,
        'top_genres': top_genres,
        'recent_games': recent_games,
    }

def game_list(request):
    logger.info("Entering game_list view")
    
    # Check for sort parameter
    sort_order = request.GET.get("sort")
    
    # Count total games in the database
    if sort_order == 'abc':
        total_games = Game.objects.all().order_by('name')[:1000]  # Sort alphabetically
    else:
        total_games = Game.objects.all()[:1000]  # Default order
    
    logger.info(f"Total games in database: {total_games}")

    # Set up pagination
    paginator = Paginator(total_games, 100)
    page_number = request.GET.get("page")

    for game in total_games:
       print(game.name)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    # Prepare context for the template
    context = {
        "page_obj": page_obj,
        "total_games": total_games,
        "games_count": total_games.count(),
        "games_per_page": 100,
    }
    
    return render(request, 'game_list.html', {"page_obj": page_obj})

def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import fetch_all_igdb_games  # Ensure this is imported
import logging
import asyncio

logger = logging.getLogger(__name__)

async def fetch_all_igdb_games_sync(total_games=500):
    """ Helper function to run the async function in a sync context. """
    return await fetch_all_igdb_games(total_games)

def search_games(request):
    query = request.GET.get('q', '').strip().lower()
    print(f"Search query: '{query}'")

    try:
        # Get all games from the database
        
        all_games = Game.objects.all()

      
        # Filter games based on the query
        if query:
            results = [game for game in all_games if query in game.name.lower()]
        else:
            results = list(all_games)

        print(f"Total number of games: {len(results)}")

        # Set up pagination
        games_per_page = 20
        paginator = Paginator(results, games_per_page)
        total_pages = paginator.num_pages

        # Iterate through all pages
        all_games_count = 0
        for page_number in range(1, total_pages + 1):
            page = paginator.page(page_number)
            for game in page:
                all_games_count += 1
                # Here you can process each game as needed
                # For example, print every 10000th game:
                if all_games_count % 10000 == 0:
                    print(f"Processing game {all_games_count}: {game.name}")

        print(f"Total games processed: {all_games_count}")

        # For the actual view rendering, we'll use the requested page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'query': query,
            'total_results': len(results),
            'total_games_processed': all_games_count,
        }
        return render(request, 'search_results.html', context)

    except Exception as e:
        logger.exception(f"Failed to process games: {e}")
        context = {
            'error': str(e),
            'query': query,
        }
        return render(request, 'members/search_results.html', context)

from django.shortcuts import render, get_object_or_404

def game_detail(request, game_id):
    game = get_object_or_404(Game, igdb_id=game_id)  # Assuming igdb_id is the unique identifier
    return render(request, 'game_detail.html', {'game': game})

def genre_games(request, genre):
    games = Game.objects.filter(genre__icontains=genre).order_by('-rating')
    paginator = Paginator(games, 20)  # Show 20 games per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'members/genre_games.html', {'page_obj': page_obj, 'genre': genre})

def platform_games(request, platform):
    games = Game.objects.filter(platforms__icontains=platform).order_by('-rating')
    paginator = Paginator(games, 20)  # Show 20 games per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'members/platform_games.html', {'page_obj': page_obj, 'platform': platform})

