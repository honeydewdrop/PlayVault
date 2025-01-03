from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm, HeaderImageForm, BiographyForm, ReviewsFixedForm, StatusForm
from django.db import connection
from members.models import Profile, GameStatus, ReviewsFixed
from .utils import fetch_all_igdb_games #sam
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count
from .models import Game
from django.shortcuts import render, get_object_or_404
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

def home(request):
    print("Home view has been triggered!")
    handpicked_game_ids = [10399]
    trending_games = Game.objects.filter(id__in=handpicked_game_ids)
    print(f"Trending games: {trending_games}")
    context = {
        'trending_games': trending_games,  # Pass handpicked games to template
    }

    return render(request, 'home.html', context)

from django.shortcuts import render
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("This is a test page.")

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

logger = logging.getLogger(__name__)

def game_list(request):
    logger.info("Entering game_list view")

    # Check for sort parameter
    sort_order = request.GET.get("sort")
    queryset = Game.objects.all()

    # Filter out games with no cover image
    queryset = queryset.exclude(cover_url__isnull=True).exclude(cover_url='')

    # Apply sorting based on the parameter
    if sort_order == 'abc':
        queryset = queryset.order_by('name')  # Sort alphabetically
    elif sort_order == 'rating':
        queryset = queryset.filter(rating__isnull=False).order_by('-rating')

    games_count = queryset.count()

    # Set up pagination with 24 games per page
    paginator = Paginator(queryset, 48)  # 24 games per page
    page_number = request.GET.get("page")

    try:
        # Get the page object based on the page number from the URL
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        # In case the page number is invalid, load the last page
        page_obj = paginator.get_page(paginator.num_pages)

    # Log page information
    logger.info(f"Displaying page {page_number} of {paginator.num_pages}, showing {len(page_obj)} games.")

    # Context for template
    context = {
        "page_obj": page_obj,
        "games_count": games_count,
        "games_per_page": 48,  # Display 24 games per page
    }

    return render(request, "game_list.html", context)

@csrf_exempt  # Use this only for testing; consider using CSRF tokens in production
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    user_games = GameStatus.objects.filter(user=request.user).select_related('game')
    user_reviews = ReviewsFixed.objects.filter(user=request.user).select_related('game')

    if request.method == 'POST':
        if 'profile_picture' in request.POST:
            profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                return JsonResponse({'success': True, 'profile_picture_url': profile.profile_picture.url})
            else:
                return JsonResponse({'success': False, 'errors': profile_picture_form.errors})

        elif 'header_image' in request.POST:
            header_image_form = HeaderImageForm(request.POST, request.FILES, instance=profile)
            if header_image_form.is_valid():
                header_image_form.save()
                return JsonResponse({'success': True, 'header_image_url': profile.header_image.url})
            else:
                return JsonResponse({'success': False, 'errors': header_image_form.errors})

        elif 'biography_form' in request.POST:
            biography_form = BiographyForm(request.POST, instance=profile)
            if biography_form.is_valid():
                biography_form.save()
                return JsonResponse({'success': True, 'biography_form': profile.biography})
            else:
                return JsonResponse({'success': False, 'errors': biography_form.errors})

    return render(request, 'profile.html', {'profile': profile, 'user_games': user_games, 'user_reviews': user_reviews})

async def fetch_all_igdb_games_sync(total_games=500):
    """ Helper function to run the async function in a sync context. """
    return await fetch_all_igdb_games(total_games)

from django.core.paginator import Paginator, EmptyPage

def search_games(request):
    query = request.GET.get('q', '').strip().lower()
    print(f"Search query: '{query}'")

    try:
        # Get all games from the database
        queryset = Game.objects.all()

        # Filter games based on the query
        if query:
            queryset = queryset.exclude(cover_url__isnull=True).exclude(cover_url='')
            queryset = queryset.filter(name__icontains=query)

        print(f"Total number of games matching query: {queryset.count()}")

        # Set up pagination
        games_per_page = 48
        paginator = Paginator(queryset, games_per_page)
        page_number = request.GET.get("page")

        try:
            # Get the page object based on the page number from the URL
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            # If the page number is invalid, load the last page
            page_obj = paginator.get_page(paginator.num_pages)

        # Context for the template
        context = {
            'page_obj': page_obj,
            'query': query,  # Pass the query as 'query'
            'total_results': queryset.count(),
        }

        return render(request, 'search_results.html', context)

    except Exception as e:
        logger.exception(f"Failed to process games: {e}")
        context = {
            'error': str(e),
            'query': query,
        }
        return render(request, 'search_results.html', context)



def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    screenshots = game.game_screenshots.all()  # Fetch all screenshots related to the game
    header_image = screenshots.first().url if screenshots.exists() else None  # Get the first screenshot URL for the header
    companies = game.companies.all()
    reviews = game.reviews.all()
    context = {
        'game': game,
        'screenshots': screenshots,  # Pass all screenshots to the template
        'header_image': header_image,  # Pass the header image to the template
        'company': companies,
        'reviews': reviews
    }
    return render(request, 'game_detail.html', context)

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

def get_all_reviews(request, game_id):
    if request.method == "GET":
        reviews = ReviewsFixed.objects.filter(game_id=game_id).select_related('user')  # Adjust based on your model
        reviews_data = [
            {
                "username": review.user.username,
                "reviewtext": review.reviewtext,
                "rating": review.rating,
            }
            for review in reviews
        ]
        return JsonResponse({"reviews": reviews_data})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def submit_review(request):
       if request.method == 'POST':
           print("Form submitted")  # Debugging line
           form = ReviewsFixedForm(request.POST)
           if form.is_valid():
               print("Form is valid")  # Debugging line
               try:
                   review = form.save(commit=False)
                   review.user = request.user
                   review.game = get_object_or_404(Game, id=request.POST.get('game_id'))
                   review.save()
                   return JsonResponse({
                       'username': review.user.username,
                       'reviewtext': review.reviewtext,
                       'rating': review.rating,
                   })
               except Exception as e:
                   print("Error saving review:", e)  # Print any errors that occur
                   return JsonResponse({'error': 'Error saving review. Must be logged in.'}, status=500)
           else:
               print("Form errors:", form.errors)  # Print form errors for debugging
               return JsonResponse({'error': 'Invalid form submission', 'details': form.errors}, status=400)
       return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def progress_view(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            # Get the game object
            game = get_object_or_404(Game, id=request.POST.get('game_id'))

            # Try to get the existing status for this user and game
            game_status, created = GameStatus.objects.get_or_create(user=request.user, game=game)

            # If the status already exists, update it
            if not created:
                game_status.status = form.cleaned_data['status']
                game_status.save()

            # If the status was newly created, set the user and game
            else:
                game_status.user = request.user
                game_status.game = game
                game_status.status = form.cleaned_data['status']
                game_status.save()

            return JsonResponse({
                'status': game_status.status,  # Return the selected status
                'message': 'Status updated successfully' if not created else 'Status created successfully',
            })
        else:
            return JsonResponse({'error': 'Invalid form data', 'details': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def my_reviews_view(request):
    user_reviews = ReviewsFixed.objects.filter(user=request.user)  # Replace `Review` with your model name
    return render(request, 'members/profile.html', {'reviews': user_reviews})