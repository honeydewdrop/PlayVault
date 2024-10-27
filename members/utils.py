import asyncio
import aiohttp
import logging
from django.conf import settings
from django.utils import timezone
import time
from django.db.utils import OperationalError
from .models import Game
from django.db import transaction

logger = logging.getLogger(__name__)


import datetime
from django.utils import timezone

def convert_timestamp(timestamp):
    try:
        return datetime.datetime.fromtimestamp(timestamp).date()
    except (OSError, ValueError, TypeError):
        return None

def truncate_string(s, max_length):
    return s[:max_length] if s else s

async def save_games_to_db(games):
    @transaction.atomic
    def save_batch(batch):
        for game in batch:
            Game.objects.update_or_create(
                igdb_id=game['id'],
                defaults={
                    'name': game['name'],
                    'cover_url': game.get('cover', {}).get('url'),
                    'genre': ', '.join([genre['name'] for genre in game.get('genres', [])]),
                    'platforms': ', '.join([platform['name'] for platform in game.get('platforms', [])]),
                    'description': game.get('summary'),
                    'release_date': convert_timestamp(game.get('first_release_date')),
                    'rating': game.get('rating'),
                    'last_updated': timezone.now()
                }
            )

    # Process in batches of 100
    batch_size = 100
    for i in range(0, len(games), batch_size):
        batch = games[i:i+batch_size]
        await asyncio.to_thread(save_batch, batch)

async def fetch_all_igdb_games(total_games=286000):
    headers = {
        'Client-ID': '5fx0c2tdp25zr3fuazhlqmwvezok4f',
        'Authorization': 'Bearer 9xs6a5rq9q9i37q84ca5w82uasrwt9',
    }

    limit = 500  # IGDB allows up to 500 results per request
    all_games = []
    offsets = range(0, total_games, limit)
    max_requests_per_second = 4  # IGDB rate limit

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(max_requests_per_second)
        tasks = []

        async def fetch_games(offset):
            async with semaphore:
                url = 'https://api.igdb.com/v4/games'
                data = f'''fields id, name, cover.url, genres.name, platforms.name, summary, first_release_date, rating, involved_companies, age_ratings. screenshots;
                           limit {limit};
                           offset {offset};'''
                
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        games = await response.json()
                        all_games.extend(games)
                        print(f"Fetched games {offset} to {offset+limit}")
                    else:
                        print(f"Error fetching games: {response.status}")
                
                await asyncio.sleep(1/max_requests_per_second)  # Ensure we don't exceed rate limit

        for offset in offsets:
            task = asyncio.create_task(fetch_games(offset))
            tasks.append(task)

        await asyncio.gather(*tasks)

    print(f"Total games fetched: {len(all_games)}")
    return all_games