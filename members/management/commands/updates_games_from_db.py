from django.core.management.base import BaseCommand
from django.db import transaction
from members.models import Game

class Command(BaseCommand):
    help = 'Updates game information using data from the database'

    def handle(self, *args, **options):
        total_games = Game.objects.count()
        self.stdout.write(f"Updating {total_games} games...")

        # Example: Update all games' ratings (you can modify this based on your needs)
        with transaction.atomic():
            for game in Game.objects.all():
                # Perform your update logic here
                # For example, let's say we want to normalize ratings to a 0-10 scale
                if game.rating:
                    game.rating = min(game.rating / 10, 10)
                game.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {total_games} games"))