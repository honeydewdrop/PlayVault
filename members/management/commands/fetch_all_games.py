import asyncio
from django.core.management.base import BaseCommand
from django.db import transaction
from members.models import Game
from members.utils import fetch_all_igdb_games
import datetime
from requests import post

class Command(BaseCommand):
    help = 'Fetches all games from IGDB API and stores them in the database'

    def handle(self, *args, **options):
        response = post(
            'https://api.igdb.com/v4/games',
            headers = {
            # shhhhhhhhh!
            },
            data='fields change_date,change_date_category,changed_company_id,checksum,country,created_at,description,developed,logo,name,parent,published,slug,start_date,start_date_category,updated_at,url,websites;'
        )


    def handle(self, *args, **options):
        asyncio.run(self.async_handle(*args, **options))

    async def async_handle(self, *args, **options):
        self.stdout.write("Fetching all games from IGDB API...")
        games_data = await fetch_all_igdb_games()
        
        self.stdout.write(f"Fetched {len(games_data)} games. Storing in database...")
        await self.store_games(games_data)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully stored {len(games_data)} games in the database"))

    async def store_games(self, games_data):
        batch_size = 1000
        for i in range(0, len(games_data), batch_size):
            batch = games_data[i:i+batch_size]
            games_to_create = []
            for game in batch:
                try:
                    games_to_create.append(Game(
                        igdb_id=game['id'],
                        name=game['name'],
                        cover_url=game.get('cover', {}).get('url'),
                        genre=', '.join([genre['name'] for genre in game.get('genres', [])]),
                        platforms=', '.join([platform['name'] for platform in game.get('platforms', [])]),
                        description=game.get('summary'),
                        release_date=self.convert_timestamp(game.get('first_release_date')),
                        rating=game.get('rating')
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error processing game {game.get('id')}: {str(e)}"))
            
            await self.bulk_create_games(games_to_create)
            self.stdout.write(f"Stored games {i+1} to {i+len(batch)}")

    @staticmethod
    async def bulk_create_games(games):
        await asyncio.to_thread(Game.objects.bulk_create, games, ignore_conflicts=True)

    @staticmethod
    def convert_timestamp(timestamp):
        if timestamp:
            try:
                # Convert milliseconds to seconds if necessary
                if timestamp > 1e10:  # Assuming timestamps after year 2286 are in milliseconds
                    timestamp = timestamp / 1000
                return datetime.datetime.fromtimestamp(timestamp).date()
            except (ValueError, TypeError, OSError):
                return None
        return None